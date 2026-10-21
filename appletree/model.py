"""Transparent Gaussian naive Bayes pixel baseline, implemented with NumPy.

Assumes conditionally independent Gaussian feature channels. This is an initial
baseline, not a claim that this assumption represents orchard images well.
"""
import numpy as np


def features(rgb, depth=None):
    """Return normalized RGB, optionally followed by three encoded-depth channels.

    Inputs must be matching HxWx3 uint8 arrays. Returns (H*W)x3 or x6 float64.
    No camera calibration, physical distance or invalid-depth rule is inferred.
    """
    arrays = [rgb] if depth is None else [rgb, depth]
    if any(a.shape != rgb.shape or a.ndim != 3 or a.shape[2] != 3 or a.dtype != np.uint8 for a in arrays):
        raise ValueError("Expected matching HxWx3 uint8 images")
    return np.concatenate([a.reshape(-1, 3) for a in arrays], axis=1).astype(float) / 255


class GaussianPixels:
    """Binary Gaussian naive Bayes with explicit variance regularisation."""

    def fit(self, x, y, variance_floor=1e-4):
        """Fit class means, variances and empirical priors; return self.

        Args:
            x: Finite NxF feature matrix.
            y: Binary N-element labels; both classes must be present.
            variance_floor: Positive variance floor to prevent singular density.
        Raises:
            ValueError: Invalid arrays, absent classes or nonpositive floor.
        """
        x, y = np.asarray(x), np.asarray(y)
        if x.ndim != 2 or y.shape != (len(x),) or not np.isfinite(x).all() or set(np.unique(y)) != {0, 1} or variance_floor <= 0:
            raise ValueError("Need finite NxF inputs, both binary classes, positive floor")
        self.mean = np.array([x[y == c].mean(0) for c in (0, 1)])
        self.var = np.array([np.maximum(x[y == c].var(0), variance_floor) for c in (0, 1)])
        self.prior = np.array([(y == c).mean() for c in (0, 1)])
        return self

    def predict_proba(self, x):
        """Return foreground probabilities using log densities for stability.

        Args:
            x: Finite NxF features with the fitted number of channels.
        Raises:
            ValueError: Unfitted model or invalid feature matrix.
        """
        x = np.asarray(x)
        if not hasattr(self, "mean") or x.ndim != 2 or x.shape[1] != self.mean.shape[1] or not np.isfinite(x).all():
            raise ValueError("Unfitted model or invalid features")
        logp = np.array([-.5 * np.sum(np.log(2 * np.pi * self.var[c]) + (x - self.mean[c]) ** 2 / self.var[c], axis=1)
                         + np.log(self.prior[c]) for c in (0, 1)])
        return 1 / (1 + np.exp(np.clip(logp[0] - logp[1], -700, 700)))
