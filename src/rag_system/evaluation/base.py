from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time


@dataclass
class Question:
    """Represents a question in the evaluation dataset"""
    id: str
    question: str
    expected_answer: str
    context: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class Answer:
    """Represents an answer from a QA system"""
    question_id: str
    answer: str
    retrieval_context: str
    method: str
    response_time: float
    metadata: Dict[str, Any] = None


@dataclass
class EvaluationResult:
    """Results of evaluating an answer"""
    question_id: str
    method: str
    exact_match: float
    f1_score: float
    rouge_l: float
    bleu_score: float
    retrieval_recall: float
    response_time: float
    metadata: Dict[str, Any] = None


@dataclass
class EvaluationSummary:
    """Summary of evaluation results across multiple questions"""
    method: str
    num_questions: int
    avg_exact_match: float
    avg_f1_score: float
    avg_rouge_l: float
    avg_bleu_score: float
    avg_retrieval_recall: float
    avg_response_time: float
    std_response_time: float
    metadata: Dict[str, Any] = None


class Metric(ABC):
    """Abstract base class for evaluation metrics"""
    
    @abstractmethod
    def compute(self, predicted: str, expected: str, context: Optional[str] = None) -> float:
        """Compute metric score"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get metric name"""
        pass


class Evaluator(ABC):
    """Abstract base class for evaluators"""
    
    @abstractmethod
    def evaluate_answer(
        self, 
        question: Question, 
        answer: Answer,
        context: Optional[str] = None
    ) -> EvaluationResult:
        """Evaluate a single answer"""
        pass
    
    @abstractmethod
    def evaluate_batch(
        self, 
        questions: List[Question], 
        answers: List[Answer]
    ) -> List[EvaluationResult]:
        """Evaluate a batch of answers"""
        pass
    
    @abstractmethod
    def summarize_results(self, results: List[EvaluationResult]) -> EvaluationSummary:
        """Summarize evaluation results"""
        pass