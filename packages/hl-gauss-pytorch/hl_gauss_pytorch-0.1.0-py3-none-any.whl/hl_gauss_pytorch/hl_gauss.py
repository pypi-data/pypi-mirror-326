from __future__ import annotations

import torch
from torch.special import erf
import torch.nn.functional as F
from torch import nn, tensor, linspace
from torch.nn import Module, ModuleList

import einx
from einops import rearrange

# helper functions

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

def log(t, eps = 1e-20):
    return t.clamp(min = eps).log()

# proposed gaussian histogram loss by Imani et al. https://arxiv.org/abs/1806.04613

class HLGaussLoss(Module):
    """
    lifted from Appendix A in https://arxiv.org/abs/2403.03950
    """

    def __init__(
        self,
        min_value,
        max_value,
        num_bins,
        sigma = None,
        default_sigma_to_bin_ratio = 2.
    ):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

        assert num_bins > 2
        self.num_bins = num_bins

        support = linspace(min_value, max_value, num_bins + 1).float()
        bin_size = support[1] - support[0]

        sigma = default(sigma, int(default_sigma_to_bin_ratio * bin_size)) # default sigma to ratio of 2. with bin size, from fig 6 of https://arxiv.org/html/2402.13425v2
        self.sigma = sigma

        self.register_buffer('support', support)
        self.register_buffer('centers', support[:-1] + (support[:-1] - support[1:]) / 2)
        self.register_buffer('sigma_times_sqrt_two', tensor(2.0).sqrt() * sigma)

    def transform_to_logprobs(self, values):
        probs = self.transform_to_probs(values)
        return log(probs)

    def transform_to_probs(self, target):
        cdf_evals = erf(einx.subtract('bins, ... -> ... bins', self.support, target) / self.sigma_times_sqrt_two)

        z = cdf_evals[..., -1] - cdf_evals[..., 0]
        bin_probs = cdf_evals[..., 1:] - cdf_evals[..., :-1]

        return einx.divide('... bins, ... -> ... bins', bin_probs, z)

    def transform_from_probs(self, probs):
        return (probs * self.centers).sum(dim = -1)

    def forward(
        self,
        logits,
        target = None
    ):
        assert logits.shape[-1] == self.num_bins

        return_loss = exists(target)

        if return_loss:
            return F.cross_entropy(logits, self.transform_to_probs(target))

        # if targets are not given, return the predicted value

        pred_probs = logits.softmax(dim = -1)

        return self.transform_from_probs(pred_probs)

# a layer that contains a projection from the embedding of a network to the predicted bins

class HLGaussLayer(Module):
    def __init__(
        self,
        dim,
        *,
        norm_embed = False,
        hl_gauss_loss: dict | HLGaussLoss | None = None,
        use_regression = False, # can be disabled to compare with regular MSE regression
        regress_activation = nn.Identity(),
    ):
        super().__init__()

        self.norm = nn.RMSNorm(dim) if norm_embed else nn.Identity()

        if isinstance(hl_gauss_loss, dict):
            hl_gauss_loss = HLGaussLoss(**hl_gauss_loss)

        self.hl_gauss_loss = hl_gauss_loss

        use_classification = not use_regression
        assert not (use_classification and not exists(hl_gauss_loss)), '`hl_gauss_loss` is not defined, only regression is permitted'

        # linear projection to either logits for classification, or single value for regression

        dim_pred = hl_gauss_loss.num_bins if use_classification else 1
        self.to_pred = nn.Linear(dim, dim_pred, bias = False)

        self.use_classification = use_classification

        # if using regression, activation to apply after the projection

        self.regress_activation = regress_activation

    def forward_mse_regression(
        self,
        embed,
        target = None
    ):
        assert not self.use_classification

        embed = self.norm(embed)

        pred_value = self.to_pred(embed)
        pred_value = self.regress_activation(pred_value)
        pred_value = rearrange(pred_value, '... 1 -> ...')

        return_loss = exists(target)

        if not return_loss:
            return pred_value

        return F.mse_loss(pred_value, target)

    def forward(
        self,
        embed,
        target = None,
        return_logits = False
    ):

        if not self.use_classification:
            assert not return_logits, 'no logits to return when using regression'
            return self.forward_mse_regression(embed, target)

        embed = self.norm(embed)
        logits = self.to_pred(embed)

        if return_logits:
            return logits

        if not exists(target):
            return self.hl_gauss_loss(logits)

        return self.hl_gauss_loss(logits, target)
