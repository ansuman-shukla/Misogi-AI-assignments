"""
OpenAI provider implementation.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
import os
from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI model provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        self.base_url = config.get('openai_base_url', 'https://api.openai.com/v1')
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    async def generate_response(
        self, 
        query: str, 
        model_type: str = 'instruct',
        model_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI models."""
        if not self.client:
            raise ValueError("OpenAI client not initialized. Check API key.")
        
        # Select model based on type
        if not model_name:
            model_name = self.get_default_model(model_type)
        
        if not model_name:
            raise ValueError(f"No available model for type: {model_type}")
        
        start_time = time.time()
        
        try:
            # Prepare request parameters
            params = self.prepare_request_params(query, model_name, **kwargs)
            
            # Make API call
            response = await self.client.chat.completions.create(**params)
            
            response_time = time.time() - start_time
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            # Extract token usage
            token_usage = {
                'input_tokens': response.usage.prompt_tokens,
                'output_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
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
        """Get available OpenAI models."""
        return {
            'base': [
                'gpt-3.5-turbo-instruct',  # Closest to base model
                'text-davinci-003'
            ],
            'instruct': [
                'gpt-3.5-turbo',
                'gpt-3.5-turbo-16k',
                'gpt-4',
                'gpt-4-turbo-preview',
                'gpt-4-turbo',
                'gpt-4o',
                'gpt-4o-mini'
            ],
            'fine-tuned': [
                'gpt-3.5-turbo-ft',  # Placeholder for fine-tuned models
                'gpt-4-ft'
            ]
        }
    
    def get_model_characteristics(self, model_name: str) -> Dict[str, Any]:
        """Get characteristics of OpenAI models."""
        characteristics = {
            'gpt-3.5-turbo': {
                'context_window': 4096,
                'training_cutoff': '2021-09',
                'strengths': ['Fast response', 'Cost-effective', 'Good general performance'],
                'use_cases': ['Chat', 'Q&A', 'Text completion'],
                'fine_tuning_strategy': 'Instruction following, human feedback (RLHF)',
                'instruction_following': 'Excellent',
                'cost_per_1k_tokens': '$0.001-0.002'
            },
            'gpt-3.5-turbo-16k': {
                'context_window': 16384,
                'training_cutoff': '2021-09',
                'strengths': ['Larger context', 'Fast response', 'Cost-effective'],
                'use_cases': ['Long document analysis', 'Extended conversations'],
                'fine_tuning_strategy': 'Instruction following, human feedback (RLHF)',
                'instruction_following': 'Excellent',
                'cost_per_1k_tokens': '$0.003-0.004'
            },
            'gpt-4': {
                'context_window': 8192,
                'training_cutoff': '2021-09',
                'strengths': ['Advanced reasoning', 'Better accuracy', 'Complex tasks'],
                'use_cases': ['Complex analysis', 'Creative writing', 'Problem solving'],
                'fine_tuning_strategy': 'Advanced RLHF, constitutional AI',
                'instruction_following': 'Outstanding',
                'cost_per_1k_tokens': '$0.03-0.06'
            },
            'gpt-4-turbo': {
                'context_window': 128000,
                'training_cutoff': '2023-12',
                'strengths': ['Large context', 'Latest training data', 'Multimodal'],
                'use_cases': ['Long document processing', 'Code analysis', 'Research'],
                'fine_tuning_strategy': 'Advanced RLHF, constitutional AI',
                'instruction_following': 'Outstanding',
                'cost_per_1k_tokens': '$0.01-0.03'
            },
            'gpt-4o': {
                'context_window': 128000,
                'training_cutoff': '2023-10',
                'strengths': ['Multimodal', 'Fast', 'Cost-effective'],
                'use_cases': ['Vision tasks', 'Audio processing', 'General chat'],
                'fine_tuning_strategy': 'Optimized RLHF for efficiency',
                'instruction_following': 'Outstanding',
                'cost_per_1k_tokens': '$0.005-0.015'
            },
            'gpt-4o-mini': {
                'context_window': 128000,
                'training_cutoff': '2023-10',
                'strengths': ['Very cost-effective', 'Fast', 'Good performance'],
                'use_cases': ['High-volume applications', 'Simple tasks', 'Prototyping'],
                'fine_tuning_strategy': 'Distilled from GPT-4o',
                'instruction_following': 'Very good',
                'cost_per_1k_tokens': '$0.0001-0.0006'
            },
            'gpt-3.5-turbo-instruct': {
                'context_window': 4096,
                'training_cutoff': '2021-09',
                'strengths': ['Text completion', 'Lower instruction bias'],
                'use_cases': ['Text completion', 'Creative writing', 'Code completion'],
                'fine_tuning_strategy': 'Minimal instruction tuning',
                'instruction_following': 'Basic',
                'cost_per_1k_tokens': '$0.0015-0.002'
            }
        }
        
        return characteristics.get(model_name, {
            'context_window': 4096,
            'training_cutoff': 'Unknown',
            'strengths': ['General purpose'],
            'use_cases': ['General tasks'],
            'fine_tuning_strategy': 'Standard',
            'instruction_following': 'Good',
            'cost_per_1k_tokens': 'Variable'
        })
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens using tiktoken."""
        try:
            import tiktoken
            
            # Get encoding for model
            if 'gpt-4' in model_name:
                encoding = tiktoken.encoding_for_model("gpt-4")
            elif 'gpt-3.5' in model_name:
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            else:
                encoding = tiktoken.get_encoding("cl100k_base")
            
            return len(encoding.encode(text))
            
        except ImportError:
            # Fallback to word-based estimation
            return len(text.split()) * 1.3  # Rough approximation
    
    def get_context_window(self, model_name: str) -> int:
        """Get context window size for OpenAI models."""
        windows = {
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384,
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-4-turbo': 128000,
            'gpt-4-turbo-preview': 128000,
            'gpt-4o': 128000,
            'gpt-4o-mini': 128000,
            'gpt-3.5-turbo-instruct': 4096,
            'text-davinci-003': 4097,
        }
        return windows.get(model_name, 4096)
    
    def get_default_model(self, model_type: str) -> str:
        """Get default OpenAI model for type."""
        defaults = {
            'base': 'gpt-3.5-turbo-instruct',
            'instruct': 'gpt-3.5-turbo',
            'fine-tuned': 'gpt-3.5-turbo-ft'
        }
        return defaults.get(model_type)
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key."""
        return self.api_key is not None and len(self.api_key.strip()) > 0
