"""
Anthropic provider implementation.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
import os
from .base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic model provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY')
        self.base_url = config.get('anthropic_base_url', 'https://api.anthropic.com')
        self.client = None
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    async def generate_response(
        self, 
        query: str, 
        model_type: str = 'instruct',
        model_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Anthropic models."""
        if not self.client:
            raise ValueError("Anthropic client not initialized. Check API key.")
        
        # Select model based on type
        if not model_name:
            model_name = self.get_default_model(model_type)
        
        if not model_name:
            raise ValueError(f"No available model for type: {model_type}")
        
        start_time = time.time()
        
        try:
            # Prepare request parameters
            max_tokens = kwargs.get('max_tokens', self.config.get('max_tokens', 1000))
            temperature = kwargs.get('temperature', self.config.get('temperature', 0.7))
            
            # Make API call
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            
            response_time = time.time() - start_time
            
            # Extract response text
            response_text = response.content[0].text if response.content else ""
            
            # Extract token usage
            token_usage = {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
                'total_tokens': response.usage.input_tokens + response.usage.output_tokens
            }
            
            return self.format_response(
                response_text=response_text,
                model_name=model_name,
                model_type=model_type,
                token_usage=token_usage,
                response_time=response_time
            )
            
        except Exception as e:
            return {
                'provider': self.provider_name,
                'model_name': model_name,
                'model_type': model_type,
                'response': f"Error: {str(e)}",
                'token_usage': {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0},
                'characteristics': {},
                'response_time': time.time() - start_time,
                'context_window': 0,
                'error': str(e)
            }
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get available Anthropic models."""
        return {
            'base': [
                # Claude base models are not publicly available
            ],
            'instruct': [
                'claude-3-haiku-20240307',
                'claude-3-sonnet-20240229',
                'claude-3-opus-20240229',
                'claude-3-5-sonnet-20240620',
                'claude-2.1',
                'claude-2.0',
                'claude-instant-1.2'
            ],
            'fine-tuned': [
                # Custom fine-tuned models would go here
            ]
        }
    
    def get_model_characteristics(self, model_name: str) -> Dict[str, Any]:
        """Get characteristics of Anthropic models."""
        characteristics = {
            'claude-3-haiku-20240307': {
                'context_window': 200000,
                'training_cutoff': '2024-02',
                'strengths': ['Fastest Claude 3', 'Cost-effective', 'Good for simple tasks'],
                'use_cases': ['Quick responses', 'Simple analysis', 'High-volume applications'],
                'fine_tuning_strategy': 'Constitutional AI, RLHF',
                'instruction_following': 'Very good',
                'cost_per_1k_tokens': '$0.00025-0.00125'
            },
            'claude-3-sonnet-20240229': {
                'context_window': 200000,
                'training_cutoff': '2024-02',
                'strengths': ['Balanced performance', 'Good reasoning', 'Versatile'],
                'use_cases': ['General assistance', 'Content creation', 'Analysis'],
                'fine_tuning_strategy': 'Constitutional AI, RLHF',
                'instruction_following': 'Excellent',
                'cost_per_1k_tokens': '$0.003-0.015'
            },
            'claude-3-opus-20240229': {
                'context_window': 200000,
                'training_cutoff': '2024-02',
                'strengths': ['Highest capability', 'Complex reasoning', 'Creative tasks'],
                'use_cases': ['Complex analysis', 'Research', 'Creative writing'],
                'fine_tuning_strategy': 'Advanced Constitutional AI, RLHF',
                'instruction_following': 'Outstanding',
                'cost_per_1k_tokens': '$0.015-0.075'
            },
            'claude-3-5-sonnet-20240620': {
                'context_window': 200000,
                'training_cutoff': '2024-04',
                'strengths': ['Latest model', 'Improved reasoning', 'Better code understanding'],
                'use_cases': ['Code analysis', 'Complex reasoning', 'Latest capabilities'],
                'fine_tuning_strategy': 'Enhanced Constitutional AI, RLHF',
                'instruction_following': 'Outstanding',
                'cost_per_1k_tokens': '$0.003-0.015'
            },
            'claude-2.1': {
                'context_window': 200000,
                'training_cutoff': '2023-04',
                'strengths': ['Large context', 'Good reasoning', 'Reduced hallucinations'],
                'use_cases': ['Long document analysis', 'Research', 'Content creation'],
                'fine_tuning_strategy': 'Constitutional AI, RLHF',
                'instruction_following': 'Very good',
                'cost_per_1k_tokens': '$0.008-0.024'
            },
            'claude-2.0': {
                'context_window': 100000,
                'training_cutoff': '2023-03',
                'strengths': ['Good general performance', 'Creative tasks'],
                'use_cases': ['General assistance', 'Writing', 'Analysis'],
                'fine_tuning_strategy': 'Constitutional AI, RLHF',
                'instruction_following': 'Good',
                'cost_per_1k_tokens': '$0.008-0.024'
            },
            'claude-instant-1.2': {
                'context_window': 100000,
                'training_cutoff': '2023-03',
                'strengths': ['Fast responses', 'Cost-effective'],
                'use_cases': ['Quick queries', 'Simple tasks', 'High-volume'],
                'fine_tuning_strategy': 'Streamlined Constitutional AI',
                'instruction_following': 'Good',
                'cost_per_1k_tokens': '$0.0008-0.0024'
            }
        }
        
        return characteristics.get(model_name, {
            'context_window': 200000,
            'training_cutoff': 'Unknown',
            'strengths': ['General purpose'],
            'use_cases': ['General tasks'],
            'fine_tuning_strategy': 'Constitutional AI',
            'instruction_following': 'Good',
            'cost_per_1k_tokens': 'Variable'
        })
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens for Anthropic models."""
        try:
            # Anthropic uses a similar tokenization to GPT models
            # This is an approximation
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except ImportError:
            # Fallback to word-based estimation
            return len(text.split()) * 1.3
    
    def get_context_window(self, model_name: str) -> int:
        """Get context window size for Anthropic models."""
        windows = {
            'claude-3-haiku-20240307': 200000,
            'claude-3-sonnet-20240229': 200000,
            'claude-3-opus-20240229': 200000,
            'claude-3-5-sonnet-20240620': 200000,
            'claude-2.1': 200000,
            'claude-2.0': 100000,
            'claude-instant-1.2': 100000,
        }
        return windows.get(model_name, 200000)
    
    def get_default_model(self, model_type: str) -> str:
        """Get default Anthropic model for type."""
        defaults = {
            'base': None,  # No public base models
            'instruct': 'claude-3-sonnet-20240229',
            'fine-tuned': None  # Custom models
        }
        return defaults.get(model_type)
    
    def validate_api_key(self) -> bool:
        """Validate Anthropic API key."""
        return self.api_key is not None and len(self.api_key.strip()) > 0
    
    def prepare_request_params(self, query: str, model_name: str, **kwargs) -> Dict[str, Any]:
        """Prepare request parameters for Anthropic API."""
        return {
            'model': model_name,
            'messages': [{'role': 'user', 'content': query}],
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 1000)),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
        }
