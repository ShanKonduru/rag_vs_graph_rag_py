from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM"""
    text: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    model: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class LLMRequest:
    """Request to LLM"""
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: int = 512
    stop: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Simple chat interface"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM is available"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        pass