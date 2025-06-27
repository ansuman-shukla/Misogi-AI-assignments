"""
Base provider class and interfaces for model providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time


@dataclass
class ModelResponse:
    """Response from a model provider."""
    provider: str
    model_name: str
    model_type: str
    response: str
    token_usage: Dict[str, int]
    characteristics: Dict[str, Any]
    response_time: float
    context_window: int
    error: Optional[str] = None


class BaseProvider(ABC):
    """Abstract base class for model providers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_name = self.__class__.__name__.lower().replace('provider', '')
    
    @abstractmethod
    async def generate_response(
        self, 
        query: str, 
        model_type: str = 'instruct',
        model_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from the model.
        
        Args:
            query: Input query
            model_type: Type of model (base, instruct, fine-tuned)
            model_name: Specific model name (optional)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing response and metadata
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> Dict[str, List[str]]:
        """
        Get available models for this provider.
        
        Returns:
            Dictionary mapping model types to available models
        """
        pass
    
    @abstractmethod
    def get_model_characteristics(self, model_name: str) -> Dict[str, Any]:
        """
        Get characteristics of a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary containing model characteristics
        """
        pass
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """
        Count tokens in text for the given model.
        
        Args:
            text: Text to count tokens for
            model_name: Model name for tokenization
            
        Returns:
            Number of tokens
        """
        # Basic word-based estimation (should be overridden by providers)
        return len(text.split())
    
    def validate_api_key(self) -> bool:
        """
        Validate API key for this provider.
        
        Returns:
            True if API key is valid
        """
        api_key = self.config.get(f'{self.provider_name}_api_key')
        return api_key is not None and len(api_key.strip()) > 0
    
    def format_response(
        self, 
        response_text: str, 
        model_name: str, 
        model_type: str,
        token_usage: Dict[str, int],
        response_time: float
    ) -> Dict[str, Any]:
        """
        Format response in standard format.
        
        Args:
            response_text: Generated response text
            model_name: Name of the model used
            model_type: Type of model used
            token_usage: Token usage information
            response_time: Time taken for response
            
        Returns:
            Formatted response dictionary
        """
        return {
            'provider': self.provider_name,
            'model_name': model_name,
            'model_type': model_type,
            'response': response_text,
            'token_usage': token_usage,
            'characteristics': self.get_model_characteristics(model_name),
            'response_time': response_time,
            'context_window': self.get_context_window(model_name),
            'timestamp': time.time()
        }
    
    def get_context_window(self, model_name: str) -> int:
        """
        Get context window size for a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Context window size in tokens
        """
        # Default context window sizes (should be overridden)
        default_windows = {
            'gpt-3.5-turbo': 4096,
            'gpt-4': 8192,
            'gpt-4-turbo': 128000,
            'claude-3-haiku': 200000,
            'claude-3-sonnet': 200000,
            'claude-3-opus': 200000,
        }
        return default_windows.get(model_name, 4096)
    
    def get_default_model(self, model_type: str) -> str:
        """
        Get default model for a given type.
        
        Args:
            model_type: Type of model (base, instruct, fine-tuned)
            
        Returns:
            Default model name for the type
        """
        available_models = self.get_available_models()
        models = available_models.get(model_type, [])
        return models[0] if models else None
    
    def prepare_request_params(self, query: str, model_name: str, **kwargs) -> Dict[str, Any]:
        """
        Prepare request parameters for API call.
        
        Args:
            query: Input query
            model_name: Model name
            **kwargs: Additional parameters
            
        Returns:
            Request parameters
        """
        return {
            'model': model_name,
            'messages': [{'role': 'user', 'content': query}],
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 1000)),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
        }
