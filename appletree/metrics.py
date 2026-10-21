"""Binary segmentation metrics with explicitly defined empty-mask behaviour."""
import numpy as np


def confusion(target, prediction):
    """Return [TP, FP, FN, TN] counts for equal-shaped binary arrays.

    Raises ValueError for nonbinary inputs or different shapes.
    """
    target, prediction = np.asarray(target), np.asarray(prediction)
    if target.shape != prediction.shape or any(not set(np.unique(a)).issubset({0, 1}) for a in (target, prediction)):
        raise ValueError("Expected equal-shaped binary masks")
    t, p = target.astype(bool), prediction.astype(bool)
    return np.array([(t & p).sum(), (~t & p).sum(), (t & ~p).sum(), (~t & ~p).sum()], dtype=np.int64)


def scores(counts):
    """Return IoU, Dice, precision and recall from TP/FP/FN/TN.

    Both-empty masks receive IoU/Dice=1. Undefined precision/recall receive 0.
    """
    tp, fp, fn, tn = map(int, counts)
    return {"iou": tp / (tp + fp + fn) if tp + fp + fn else 1.,
            "dice": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 1.,
            "precision": tp / (tp + fp) if tp + fp else 0.,
            "recall": tp / (tp + fn) if tp + fn else 0.}
