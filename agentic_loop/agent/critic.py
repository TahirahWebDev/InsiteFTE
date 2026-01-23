"""
Critic module for the Gold Tier Agentic Loop system.
"""

import asyncio
from typing import Dict, Any
from ..utils.logger import get_logger


class CriticModule:
    """
    Component that reviews AI output for quality before moving to 03_Pending_Approval.
    """
    
    def __init__(self):
        """Initialize the critic module."""
        self.logger = get_logger()
        self.quality_threshold = 0.7  # Default quality threshold (0.0 to 1.0)
    
    async def evaluate_quality(self, content: str, criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate the quality of content based on specified criteria.
        
        Args:
            content: The content to evaluate
            criteria: Optional criteria to evaluate against (default: use standard criteria)
            
        Returns:
            Dictionary with evaluation results
        """
        self.logger.info("Starting quality evaluation...")
        
        # Simulate AI processing time
        await asyncio.sleep(0.3)
        
        # Set default criteria if none provided
        if criteria is None:
            criteria = {
                "completeness": True,
                "accuracy": True,
                "relevance": True,
                "clarity": True,
                "consistency": True
            }
        
        # Perform evaluation based on criteria
        evaluation_results = {
            "content_length": len(content),
            "completeness_score": self._evaluate_completeness(content),
            "accuracy_score": self._evaluate_accuracy(content),
            "relevance_score": self._evaluate_relevance(content),
            "clarity_score": self._evaluate_clarity(content),
            "consistency_score": self._evaluate_consistency(content),
            "overall_quality_score": 0.0,
            "issues_found": [],
            "suggestions": []
        }
        
        # Calculate overall quality score based on enabled criteria
        scores_to_consider = []
        if criteria.get("completeness", True):
            scores_to_consider.append(evaluation_results["completeness_score"])
        if criteria.get("accuracy", True):
            scores_to_consider.append(evaluation_results["accuracy_score"])
        if criteria.get("relevance", True):
            scores_to_consider.append(evaluation_results["relevance_score"])
        if criteria.get("clarity", True):
            scores_to_consider.append(evaluation_results["clarity_score"])
        if criteria.get("consistency", True):
            scores_to_consider.append(evaluation_results["consistency_score"])
        
        if scores_to_consider:
            evaluation_results["overall_quality_score"] = sum(scores_to_consider) / len(scores_to_consider)
        
        # Identify issues and provide suggestions
        evaluation_results["issues_found"] = self._identify_issues(content, evaluation_results)
        evaluation_results["suggestions"] = self._generate_suggestions(evaluation_results)
        
        self.logger.info(f"Quality evaluation completed with overall score: {evaluation_results['overall_quality_score']:.2f}")
        return evaluation_results
    
    def _evaluate_completeness(self, content: str) -> float:
        """
        Evaluate how complete the content is.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Completeness score (0.0 to 1.0)
        """
        # Simple heuristic: longer content is more likely to be complete
        # In a real implementation, this would use more sophisticated analysis
        if len(content) < 100:
            return 0.3  # Too short
        elif len(content) < 500:
            return 0.6  # Medium length
        elif len(content) < 1000:
            return 0.8  # Good length
        else:
            return 0.9  # Very comprehensive
    
    def _evaluate_accuracy(self, content: str) -> float:
        """
        Evaluate the accuracy of the content.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Accuracy score (0.0 to 1.0)
        """
        # Simple heuristic: check for common indicators of uncertainty
        # In a real implementation, this would verify facts against trusted sources
        uncertain_indicators = ["maybe", "perhaps", "might", "could", "possibly", "likely", "probably"]
        uncertain_count = sum(1 for indicator in uncertain_indicators if indicator in content.lower())
        
        # Lower score if there are many uncertain indicators
        if uncertain_count > 5:
            return 0.4
        elif uncertain_count > 2:
            return 0.7
        else:
            return 0.9
    
    def _evaluate_relevance(self, content: str) -> float:
        """
        Evaluate how relevant the content is to the original task.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        # This would typically compare content to original task requirements
        # For now, we'll return a medium-high score
        return 0.8
    
    def _evaluate_clarity(self, content: str) -> float:
        """
        Evaluate how clear and understandable the content is.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Clarity score (0.0 to 1.0)
        """
        # Simple heuristic: shorter sentences and paragraphs tend to be clearer
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len(sentences), 1)
        
        if avg_sentence_length > 25:
            return 0.5  # Too long sentences
        elif avg_sentence_length > 15:
            return 0.7  # Medium length sentences
        else:
            return 0.9  # Good sentence length
    
    def _evaluate_consistency(self, content: str) -> float:
        """
        Evaluate the consistency of the content.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Consistency score (0.0 to 1.0)
        """
        # Simple heuristic: check for repeated contradictions
        # In a real implementation, this would analyze for logical consistency
        content_lower = content.lower()
        
        # Look for common contradiction patterns
        contradiction_patterns = [
            ("on one hand", "on the other"),
            ("first", "second", "but"),
            ("we recommend", "however", "not")
        ]
        
        contradictions_found = 0
        for pattern in contradiction_patterns:
            if all(part in content_lower for part in pattern):
                contradictions_found += 1
        
        if contradictions_found > 2:
            return 0.4
        elif contradictions_found > 0:
            return 0.7
        else:
            return 0.9
    
    def _identify_issues(self, content: str, evaluation_results: Dict[str, Any]) -> list:
        """
        Identify specific issues in the content based on evaluation results.
        
        Args:
            content: The content being evaluated
            evaluation_results: The results of the quality evaluation
            
        Returns:
            List of identified issues
        """
        issues = []
        
        if evaluation_results["completeness_score"] < 0.6:
            issues.append("Content appears to be incomplete or lacks detail")
        
        if evaluation_results["accuracy_score"] < 0.6:
            issues.append("Content contains uncertain language or potential inaccuracies")
        
        if evaluation_results["clarity_score"] < 0.6:
            issues.append("Content has long sentences or complex structure that hurts readability")
        
        if evaluation_results["consistency_score"] < 0.6:
            issues.append("Content contains contradictions or inconsistent information")
        
        # Check for other common issues
        if len(content) < 100:
            issues.append("Content is very brief and may lack sufficient detail")
        
        return issues
    
    def _generate_suggestions(self, evaluation_results: Dict[str, Any]) -> list:
        """
        Generate suggestions for improving the content based on evaluation results.
        
        Args:
            evaluation_results: The results of the quality evaluation
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        if evaluation_results["completeness_score"] < 0.6:
            suggestions.append("Consider expanding the content with more details and examples")
        
        if evaluation_results["accuracy_score"] < 0.6:
            suggestions.append("Verify facts and reduce use of uncertain language")
        
        if evaluation_results["clarity_score"] < 0.6:
            suggestions.append("Break down long sentences and simplify complex phrases")
        
        if evaluation_results["overall_quality_score"] < self.quality_threshold:
            suggestions.append(f"Overall quality is below threshold ({self.quality_threshold}), consider major revisions")
        
        if not suggestions:
            suggestions.append("Content meets quality standards")
        
        return suggestions
    
    async def should_approve(self, evaluation_results: Dict[str, Any]) -> bool:
        """
        Determine if the content should be approved based on quality evaluation.
        
        Args:
            evaluation_results: The results of the quality evaluation
            
        Returns:
            True if content should be approved, False otherwise
        """
        overall_score = evaluation_results["overall_quality_score"]
        
        if overall_score >= self.quality_threshold:
            self.logger.info(f"Content approved: quality score {overall_score:.2f} meets threshold {self.quality_threshold}")
            return True
        else:
            self.logger.info(f"Content rejected: quality score {overall_score:.2f} below threshold {self.quality_threshold}")
            return False
    
    def set_quality_threshold(self, threshold: float):
        """
        Set the quality threshold for approval decisions.
        
        Args:
            threshold: The new quality threshold (0.0 to 1.0)
        """
        if 0.0 <= threshold <= 1.0:
            self.quality_threshold = threshold
            self.logger.info(f"Quality threshold set to {threshold}")
        else:
            raise ValueError("Quality threshold must be between 0.0 and 1.0")