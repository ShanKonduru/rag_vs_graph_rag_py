import statistics
import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base import (
    Question, Answer, EvaluationResult, EvaluationSummary, 
    Metric, Evaluator
)
from .metrics import (
    ExactMatchMetric, F1Metric, RougeLMetric, BleuMetric, 
    RetrievalRecallMetric
)


logger = logging.getLogger(__name__)


class StandardEvaluator(Evaluator):
    """Standard evaluator using multiple metrics"""
    
    def __init__(self, metrics: Optional[List[Metric]] = None):
        if metrics is None:
            self.metrics = [
                ExactMatchMetric(),
                F1Metric(),
                RougeLMetric(),
                BleuMetric(),
                RetrievalRecallMetric()
            ]
        else:
            self.metrics = metrics
        
        self.metric_map = {metric.get_name(): metric for metric in self.metrics}
    
    def evaluate_answer(
        self, 
        question: Question, 
        answer: Answer,
        context: Optional[str] = None
    ) -> EvaluationResult:
        """Evaluate a single answer"""
        
        # Use retrieval context from answer if no context provided
        eval_context = context or answer.retrieval_context
        
        # Compute all metrics
        scores = {}
        for metric in self.metrics:
            try:
                score = metric.compute(
                    predicted=answer.answer,
                    expected=question.expected_answer,
                    context=eval_context
                )
                scores[metric.get_name()] = score
            except Exception as e:
                logger.warning(f"Error computing {metric.get_name()} for question {question.id}: {e}")
                scores[metric.get_name()] = 0.0
        
        # Create evaluation result
        result = EvaluationResult(
            question_id=question.id,
            method=answer.method,
            exact_match=scores.get('exact_match', 0.0),
            f1_score=scores.get('f1_score', 0.0),
            rouge_l=scores.get('rouge_l', 0.0),
            bleu_score=scores.get('bleu_score', 0.0),
            retrieval_recall=scores.get('retrieval_recall', 0.0),
            response_time=answer.response_time,
            metadata={
                'question_text': question.question,
                'predicted_answer': answer.answer,
                'expected_answer': question.expected_answer,
                'all_scores': scores
            }
        )
        
        return result
    
    def evaluate_batch(
        self, 
        questions: List[Question], 
        answers: List[Answer],
        max_workers: int = 4
    ) -> List[EvaluationResult]:
        """Evaluate a batch of answers"""
        
        # Create question lookup
        question_map = {q.id: q for q in questions}
        
        results = []
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit evaluation tasks
            future_to_answer = {
                executor.submit(
                    self.evaluate_answer, 
                    question_map[answer.question_id], 
                    answer
                ): answer 
                for answer in answers 
                if answer.question_id in question_map
            }
            
            # Collect results
            for future in as_completed(future_to_answer):
                answer = future_to_answer[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error evaluating answer for question {answer.question_id}: {e}")
        
        logger.info(f"Evaluated {len(results)} answers")
        return results
    
    def summarize_results(self, results: List[EvaluationResult]) -> EvaluationSummary:
        """Summarize evaluation results"""
        
        if not results:
            return EvaluationSummary(
                method="unknown",
                num_questions=0,
                avg_exact_match=0.0,
                avg_f1_score=0.0,
                avg_rouge_l=0.0,
                avg_bleu_score=0.0,
                avg_retrieval_recall=0.0,
                avg_response_time=0.0,
                std_response_time=0.0
            )
        
        # Group by method
        method_results = {}
        for result in results:
            if result.method not in method_results:
                method_results[result.method] = []
            method_results[result.method].append(result)
        
        summaries = []
        for method, method_results_list in method_results.items():
            summary = self._summarize_method_results(method, method_results_list)
            summaries.append(summary)
        
        return summaries if len(summaries) > 1 else summaries[0]
    
    def _summarize_method_results(
        self, 
        method: str, 
        results: List[EvaluationResult]
    ) -> EvaluationSummary:
        """Summarize results for a single method"""
        
        # Extract metric values
        exact_matches = [r.exact_match for r in results]
        f1_scores = [r.f1_score for r in results]
        rouge_scores = [r.rouge_l for r in results]
        bleu_scores = [r.bleu_score for r in results]
        recall_scores = [r.retrieval_recall for r in results]
        response_times = [r.response_time for r in results]
        
        # Compute averages
        avg_exact_match = statistics.mean(exact_matches)
        avg_f1_score = statistics.mean(f1_scores)
        avg_rouge_l = statistics.mean(rouge_scores)
        avg_bleu_score = statistics.mean(bleu_scores)
        avg_retrieval_recall = statistics.mean(recall_scores)
        avg_response_time = statistics.mean(response_times)
        
        # Compute standard deviation for response time
        std_response_time = statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        
        return EvaluationSummary(
            method=method,
            num_questions=len(results),
            avg_exact_match=avg_exact_match,
            avg_f1_score=avg_f1_score,
            avg_rouge_l=avg_rouge_l,
            avg_bleu_score=avg_bleu_score,
            avg_retrieval_recall=avg_retrieval_recall,
            avg_response_time=avg_response_time,
            std_response_time=std_response_time,
            metadata={
                'score_ranges': {
                    'exact_match': (min(exact_matches), max(exact_matches)),
                    'f1_score': (min(f1_scores), max(f1_scores)),
                    'rouge_l': (min(rouge_scores), max(rouge_scores)),
                    'bleu_score': (min(bleu_scores), max(bleu_scores)),
                    'retrieval_recall': (min(recall_scores), max(recall_scores))
                }
            }
        )
    
    def compare_methods(
        self, 
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Compare different methods"""
        
        # Group results by method
        method_results = {}
        for result in results:
            if result.method not in method_results:
                method_results[result.method] = []
            method_results[result.method].append(result)
        
        # Summarize each method
        method_summaries = {}
        for method, method_results_list in method_results.items():
            method_summaries[method] = self._summarize_method_results(method, method_results_list)
        
        # Find best performing method for each metric
        best_methods = {}
        metrics = ['avg_exact_match', 'avg_f1_score', 'avg_rouge_l', 'avg_bleu_score', 'avg_retrieval_recall']
        
        for metric in metrics:
            best_score = -1
            best_method = None
            for method, summary in method_summaries.items():
                score = getattr(summary, metric)
                if score > best_score:
                    best_score = score
                    best_method = method
            best_methods[metric] = (best_method, best_score)
        
        # Performance comparison table
        comparison_table = {}
        for method, summary in method_summaries.items():
            comparison_table[method] = {
                'exact_match': summary.avg_exact_match,
                'f1_score': summary.avg_f1_score,
                'rouge_l': summary.avg_rouge_l,
                'bleu_score': summary.avg_bleu_score,
                'retrieval_recall': summary.avg_retrieval_recall,
                'response_time': summary.avg_response_time,
                'num_questions': summary.num_questions
            }
        
        return {
            'method_summaries': method_summaries,
            'best_methods': best_methods,
            'comparison_table': comparison_table,
            'total_questions': len(results)
        }