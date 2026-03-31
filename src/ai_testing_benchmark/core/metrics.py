"""
Metrics calculation utilities.
"""

from typing import List, Dict, Any, Optional, Callable
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    mean_squared_error,
    mean_absolute_error
)


class MetricsCalculator:
    """
    Utility class for calculating various evaluation metrics.
    """

    @staticmethod
    def accuracy(y_true: List, y_pred: List) -> float:
        """Calculate accuracy."""
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def f1_score(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """
        Calculate F1 score.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            average: Averaging method ('micro', 'macro', 'weighted', 'binary')
            zero_division: Value to return when there is no positive predictions
        """
        return f1_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def precision(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """Calculate precision."""
        return precision_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def recall(
        y_true: List,
        y_pred: List,
        average: str = "weighted",
        zero_division: int = 0
    ) -> float:
        """Calculate recall."""
        return recall_score(y_true, y_pred, average=average, zero_division=zero_division)

    @staticmethod
    def roc_auc(
        y_true: List,
        y_pred_proba: List,
        multi_class: str = "ovr"
    ) -> float:
        """Calculate ROC AUC score."""
        return roc_auc_score(y_true, y_pred_proba, multi_class=multi_class)

    @staticmethod
    def mean_squared_error(y_true: List, y_pred: List) -> float:
        """Calculate MSE."""
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def mean_absolute_error(y_true: List, y_pred: List) -> float:
        """Calculate MAE."""
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def rmse(y_true: List, y_pred: List) -> float:
        """Calculate RMSE."""
        return np.sqrt(mean_squared_error(y_true, y_pred))

    @staticmethod
    def mape(y_true: List, y_pred: List) -> float:
        """Calculate MAPE (Mean Absolute Percentage Error)."""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # Avoid division by zero
        mask = y_true != 0
        if not mask.any():
            return 0.0

        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    @staticmethod
    def bleu_score(
        reference: str,
        hypothesis: str,
        n_gram: int = 4
    ) -> float:
        """
        Calculate BLEU score (simplified version).

        For production use, consider using sacrebleu or nltk.translate.bleu_score.
        """
        from collections import Counter

        reference_tokens = reference.lower().split()
        hypothesis_tokens = hypothesis.lower().split()

        if len(hypothesis_tokens) == 0:
            return 0.0

        # Calculate n-gram precision
        precisions = []
        for i in range(1, min(n_gram + 1, 5)):
            ref_ngrams = Counter(self._get_ngrams(reference_tokens, i))
            hyp_ngrams = Counter(self._get_ngrams(hypothesis_tokens, i))

            overlap = sum((ref_ngrams & hyp_ngrams).values())
            total = sum(hyp_ngrams.values())

            if total == 0:
                precisions.append(0.0)
            else:
                precisions.append(overlap / total)

        # Calculate brevity penalty
        ref_len = len(reference_tokens)
        hyp_len = len(hypothesis_tokens)

        if hyp_len >= ref_len:
            bp = 1.0
        else:
            bp = np.exp(1 - ref_len / hyp_len) if hyp_len > 0 else 0.0

        # Geometric mean of precisions
        if all(p == 0 for p in precisions):
            return 0.0

        geo_mean = np.exp(np.mean([np.log(p) if p > 0 else -np.inf for p in precisions]))

        return bp * geo_mean

    @staticmethod
    def _get_ngrams(tokens: List[str], n: int) -> List[tuple]:
        """Get n-grams from token list."""
        return list(zip(*[tokens[i:] for i in range(n)]))

    @staticmethod
    def rouge_l(
        reference: str,
        hypothesis: str,
        beta: float = 1.0
    ) -> float:
        """
        Calculate ROUGE-L (Longest Common Subsequence) score.

        Simplified version - for production use sacrebleu.
        """
        reference_tokens = reference.lower().split()
        hypothesis_tokens = hypothesis.lower().split()

        lcs_length = MetricsCalculator._lcs_length(reference_tokens, hypothesis_tokens)

        if lcs_length == 0:
            return 0.0

        precision = lcs_length / len(hypothesis_tokens) if hypothesis_tokens else 0
        recall = lcs_length / len(reference_tokens) if reference_tokens else 0

        if precision + recall == 0:
            return 0.0

        f_score = (1 + beta**2) * precision * recall / (beta**2 * precision + recall)

        return f_score

    @staticmethod
    def _lcs_length(seq1: List, seq2: List) -> int:
        """Calculate length of longest common subsequence."""
        m, n = len(seq1), len(seq2)

        # Space-optimized LCS
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev, curr = curr, [0] * (n + 1)

        return prev[n]

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    @staticmethod
    def spearman_correlation(rank1: List[float], rank2: List[float]) -> float:
        """Calculate Spearman rank correlation coefficient."""
        from scipy.stats import spearmanr
        return spearmanr(rank1, rank2)[0]

    @staticmethod
    def aggregate_scores(
        scores: List[float],
        method: str = "mean"
    ) -> float:
        """
        Aggregate multiple scores.

        Args:
            scores: List of scores
            method: Aggregation method ('mean', 'median', 'min', 'max', 'harmonic')
        """
        if not scores:
            return 0.0

        if method == "mean":
            return np.mean(scores)
        elif method == "median":
            return np.median(scores)
        elif method == "min":
            return np.min(scores)
        elif method == "max":
            return np.max(scores)
        elif method == "harmonic":
            return len(scores) / sum(1/s for s in scores if s != 0)
        else:
            return np.mean(scores)

    @staticmethod
    def percentile(
        values: List[float],
        percentile: float
    ) -> float:
        """Calculate percentile value."""
        return np.percentile(values, percentile)

    @staticmethod
    def confidence_interval(
        scores: List[float],
        confidence: float = 0.95
    ) -> tuple:
        """
        Calculate confidence interval for scores.

        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        from scipy import stats

        mean = np.mean(scores)
        sem = stats.sem(scores)
        margin = sem * stats.t.ppf((1 + confidence) / 2, len(scores) - 1)

        return (mean - margin, mean + margin)


class ThresholdEvaluator:
    """Evaluate if metrics pass specified thresholds."""

    def __init__(self, thresholds: Dict[str, float]):
        """
        Initialize with thresholds.

        Args:
            thresholds: Dictionary of metric_name -> threshold_value
        """
        self.thresholds = thresholds

    def evaluate(self, metrics: Dict[str, float]) -> Dict[str, bool]:
        """
        Evaluate if metrics pass thresholds.

        Args:
            metrics: Dictionary of metric_name -> metric_value

        Returns:
            Dictionary of metric_name -> passed
        """
        results = {}

        for metric_name, threshold in self.thresholds.items():
            value = metrics.get(metric_name)

            if value is None:
                results[metric_name] = False
            else:
                results[metric_name] = value >= threshold

        return results

    def all_passed(self, metrics: Dict[str, float]) -> bool:
        """Check if all thresholds passed."""
        return all(self.evaluate(metrics).values())

    def get_failures(self, metrics: Dict[str, float]) -> List[str]:
        """Get list of metrics that failed."""
        results = self.evaluate(metrics)
        return [name for name, passed in results.items() if not passed]
