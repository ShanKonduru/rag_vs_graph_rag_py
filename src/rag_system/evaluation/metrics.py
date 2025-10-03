import re
import string
from collections import Counter
from typing import List, Set, Optional
import numpy as np

from .base import Metric


class ExactMatchMetric(Metric):
    """Exact match metric"""
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """Compute exact match score (1.0 if exact match, 0.0 otherwise)"""
        return float(self._normalize_text(predicted) == self._normalize_text(expected))
    
    def get_name(self) -> str:
        return "exact_match"
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text


class F1Metric(Metric):
    """Token-level F1 score metric"""
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """Compute F1 score based on token overlap"""
        pred_tokens = self._tokenize(predicted)
        expected_tokens = self._tokenize(expected)
        
        if not expected_tokens:
            return 1.0 if not pred_tokens else 0.0
        
        if not pred_tokens:
            return 0.0
        
        common_tokens = Counter(pred_tokens) & Counter(expected_tokens)
        num_common = sum(common_tokens.values())
        
        if num_common == 0:
            return 0.0
        
        precision = num_common / len(pred_tokens)
        recall = num_common / len(expected_tokens)
        
        f1 = 2 * precision * recall / (precision + recall)
        return f1
    
    def get_name(self) -> str:
        return "f1_score"
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        # Simple whitespace tokenization after removing punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()


class RougeL:
    """ROUGE-L metric implementation"""
    
    def __init__(self):
        self.beta = 1.2  # Standard ROUGE-L beta parameter
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """Compute ROUGE-L score"""
        pred_tokens = self._tokenize(predicted)
        expected_tokens = self._tokenize(expected)
        
        if not expected_tokens:
            return 1.0 if not pred_tokens else 0.0
        
        if not pred_tokens:
            return 0.0
        
        # Compute LCS
        lcs_length = self._lcs_length(pred_tokens, expected_tokens)
        
        if lcs_length == 0:
            return 0.0
        
        # Compute precision and recall
        r_lcs = lcs_length / len(expected_tokens)  # Recall
        p_lcs = lcs_length / len(pred_tokens)     # Precision
        
        # Compute F-measure
        beta_sq = self.beta ** 2
        f_lcs = ((1 + beta_sq) * r_lcs * p_lcs) / (r_lcs + beta_sq * p_lcs)
        
        return f_lcs
    
    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
        """Compute length of longest common subsequence"""
        m, n = len(seq1), len(seq2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()


class RougeLMetric(Metric):
    """ROUGE-L metric wrapper"""
    
    def __init__(self):
        self.rouge_l = RougeL()
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        return self.rouge_l.compute(predicted, expected)
    
    def get_name(self) -> str:
        return "rouge_l"


class BleuMetric(Metric):
    """BLEU score metric (simplified implementation)"""
    
    def __init__(self, max_n: int = 4):
        self.max_n = max_n
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """Compute BLEU score"""
        pred_tokens = self._tokenize(predicted)
        expected_tokens = self._tokenize(expected)
        
        if not expected_tokens:
            return 1.0 if not pred_tokens else 0.0
        
        if not pred_tokens:
            return 0.0
        
        # Compute n-gram precision scores
        precision_scores = []
        for n in range(1, min(self.max_n + 1, len(pred_tokens) + 1)):
            precision = self._compute_ngram_precision(pred_tokens, expected_tokens, n)
            if precision == 0:
                return 0.0  # If any n-gram precision is 0, BLEU is 0
            precision_scores.append(precision)
        
        if not precision_scores:
            return 0.0
        
        # Geometric mean of precision scores
        bleu = np.exp(np.mean(np.log(precision_scores)))
        
        # Brevity penalty
        bp = self._brevity_penalty(pred_tokens, expected_tokens)
        
        return bp * bleu
    
    def _compute_ngram_precision(
        self, 
        pred_tokens: List[str], 
        expected_tokens: List[str], 
        n: int
    ) -> float:
        """Compute n-gram precision"""
        pred_ngrams = self._get_ngrams(pred_tokens, n)
        expected_ngrams = self._get_ngrams(expected_tokens, n)
        
        if not pred_ngrams:
            return 0.0
        
        # Count matches
        matches = 0
        expected_counts = Counter(expected_ngrams)
        
        for ngram in pred_ngrams:
            if ngram in expected_counts and expected_counts[ngram] > 0:
                matches += 1
                expected_counts[ngram] -= 1
        
        return matches / len(pred_ngrams)
    
    def _get_ngrams(self, tokens: List[str], n: int) -> List[tuple]:
        """Extract n-grams from tokens"""
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    
    def _brevity_penalty(self, pred_tokens: List[str], expected_tokens: List[str]) -> float:
        """Compute brevity penalty"""
        pred_len = len(pred_tokens)
        expected_len = len(expected_tokens)
        
        if pred_len >= expected_len:
            return 1.0
        else:
            return np.exp(1 - expected_len / pred_len)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()
    
    def get_name(self) -> str:
        return "bleu_score"


class RetrievalRecallMetric(Metric):
    """Retrieval recall metric - measures if relevant information was retrieved"""
    
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """
        Compute recall based on whether key terms from expected answer 
        appear in the retrieval context
        """
        if context is None:
            return 0.0
        
        expected_tokens = set(self._tokenize(expected))
        context_tokens = set(self._tokenize(context))
        
        if not expected_tokens:
            return 1.0
        
        # Count how many expected tokens appear in context
        retrieved_tokens = expected_tokens.intersection(context_tokens)
        
        return len(retrieved_tokens) / len(expected_tokens)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text and filter out common words"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        
        # Filter out very common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        return [token for token in tokens if token not in stop_words and len(token) > 2]
    
    def get_name(self) -> str:
        return "retrieval_recall"