import requests
import json
import time
import logging
from typing import List, Dict, Any, Optional

from .base import LLMClient, LLMRequest, LLMResponse


logger = logging.getLogger(__name__)


class OllamaClient(LLMClient):
    """Ollama LLM client"""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:11434",
        model_name: str = "llama2",
        timeout: int = 60
    ):
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.timeout = timeout
        
        # Validate connection
        if not self.is_available():
            logger.warning(f"Ollama server at {self.base_url} is not available")
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from Ollama using /api/generate endpoint"""
        
        # Convert messages to prompt format for /api/generate
        prompt = ""
        for message in request.messages:
            if message["role"] == "user":
                prompt += f"{message['content']}\n"
            elif message["role"] == "system":
                prompt = f"{message['content']}\n{prompt}"
        
        # Use the generate API format which is more widely supported
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            }
        }
        
        if request.stop:
            payload["options"]["stop"] = request.stop
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",  # Use /api/generate instead
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content from generate response
            content = result.get("response", "")
            
            return LLMResponse(
                text=content,
                model=self.model_name,
                finish_reason=result.get("done_reason"),
                metadata={
                    "total_duration": result.get("total_duration"),
                    "load_duration": result.get("load_duration"), 
                    "prompt_eval_count": result.get("prompt_eval_count"),
                    "eval_count": result.get("eval_count"),
                    "eval_duration": result.get("eval_duration")
                }
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Ollama response: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Simple chat interface"""
        
        # Handle both old and new message formats
        if isinstance(messages[0], dict) and "role" in messages[0]:
            # New format with roles
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 512),
                }
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("message", {}).get("content", "")
                
            except requests.exceptions.RequestException:
                # Fallback to generate API
                pass
        
        # Use generate API as fallback
        request = LLMRequest(
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 512),
            stop=kwargs.get("stop")
        )
        
        response = self.generate(request)
        return response.text
    
    def is_available(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": self.model_name},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting model info: {e}")
            return {"model": self.model_name, "error": str(e)}
    
    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            return models
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model if not available"""
        try:
            payload = {"name": model_name}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=300  # Longer timeout for model download
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a single prompt string"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            else:
                prompt_parts.append(content)
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def update_model(self, model_name: str) -> None:
        """Update the model name"""
        self.model_name = model_name
        logger.info(f"Updated Ollama model to: {model_name}")


class MockLLMClient(LLMClient):
    """Mock LLM client for testing"""
    
    def __init__(self, responses: Optional[List[str]] = None):
        self.responses = responses or ["This is a mock response."]
        self.call_count = 0
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate mock response"""
        response_text = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        
        return LLMResponse(
            text=response_text,
            model="mock",
            finish_reason="completed",
            metadata={"call_count": self.call_count}
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Simple chat interface"""
        request = LLMRequest(messages=messages)
        response = self.generate(request)
        return response.text
    
    def is_available(self) -> bool:
        """Always available"""
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get mock model info"""
        return {
            "model": "mock",
            "type": "mock",
            "responses_count": len(self.responses),
            "call_count": self.call_count
        }