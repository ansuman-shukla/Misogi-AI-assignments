"""
Hugging Face provider implementation.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
import os
import requests
from .base_provider import BaseProvider


class HuggingFaceProvider(BaseProvider):
    """Hugging Face model provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('huggingface_api_key') or os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = config.get('huggingface_base_url', 'https://api-inference.huggingface.co')
        self.headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
    
    async def generate_response(
        self, 
        query: str, 
        model_type: str = 'instruct',
        model_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Hugging Face models."""
        if not self.api_key:
            raise ValueError("Hugging Face API key not provided.")
        
        # Select model based on type
        if not model_name:
            model_name = self.get_default_model(model_type)
        
        if not model_name:
            raise ValueError(f"No available model for type: {model_type}")
        
        start_time = time.time()
        
        try:
            # Prepare request
            url = f"{self.base_url}/models/{model_name}"
            
            # Prepare payload based on model type
            if model_type == 'base':
                # For base models, use text generation
                payload = {
                    "inputs": query,
                    "parameters": {
                        "max_new_tokens": kwargs.get('max_tokens', self.config.get('max_tokens', 100)),
                        "temperature": kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        "return_full_text": False
                    }
                }
            else:
                # For instruct/chat models, format as chat
                if 'chat' in model_name.lower() or 'instruct' in model_name.lower():
                    formatted_query = f"<|user|>\n{query}\n<|assistant|>\n"
                else:
                    formatted_query = query
                
                payload = {
                    "inputs": formatted_query,
                    "parameters": {
                        "max_new_tokens": kwargs.get('max_tokens', self.config.get('max_tokens', 100)),
                        "temperature": kwargs.get('temperature', self.config.get('temperature', 0.7)),
                        "return_full_text": False,
                        "do_sample": True
                    }
                }
            
            # Make async request
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(url, headers=self.headers, json=payload, timeout=30)
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract response text
                if isinstance(result, list) and len(result) > 0:
                    response_text = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    response_text = result.get('generated_text', str(result))
                else:
                    response_text = str(result)
                
                # Estimate token usage (HF API doesn't always provide this)
                input_tokens = self.count_tokens(query, model_name)
                output_tokens = self.count_tokens(response_text, model_name)
                token_usage = {
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'total_tokens': input_tokens + output_tokens
                }
                
                return self.format_response(
                    response_text=response_text,
                    model_name=model_name,
                    model_type=model_type,
                    token_usage=token_usage,
                    response_time=response_time
                )
            else:
                error_msg = f"API error: {response.status_code} - {response.text}"
                raise Exception(error_msg)
                
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
        """Get available Hugging Face models."""
        return {
            'base': [
                'meta-llama/Llama-2-7b-hf',
                'meta-llama/Llama-2-13b-hf',
                'mistralai/Mistral-7B-v0.1',
                'microsoft/DialoGPT-large',
                'EleutherAI/gpt-neo-2.7B'
            ],
            'instruct': [
                'meta-llama/Llama-2-7b-chat-hf',
                'meta-llama/Llama-2-13b-chat-hf',
                'mistralai/Mistral-7B-Instruct-v0.1',
                'microsoft/DialoGPT-large',
                'HuggingFaceH4/zephyr-7b-beta',
                'openchat/openchat-3.5-1210'
            ],
            'fine-tuned': [
                'codellama/CodeLlama-7b-Python-hf',
                'codellama/CodeLlama-7b-Instruct-hf',
                'WizardLM/WizardCoder-15B-V1.0',
                'Salesforce/codegen-2B-Python',
                'bigcode/starcoderbase-1b'
            ]
        }
    
    def get_model_characteristics(self, model_name: str) -> Dict[str, Any]:
        """Get characteristics of Hugging Face models."""
        characteristics = {
            'meta-llama/Llama-2-7b-hf': {
                'context_window': 4096,
                'training_cutoff': '2023-07',
                'strengths': ['Open source', 'Good general performance', 'Commercial use'],
                'use_cases': ['Text completion', 'Research', 'Fine-tuning base'],
                'fine_tuning_strategy': 'Supervised fine-tuning',
                'instruction_following': 'Basic',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'meta-llama/Llama-2-7b-chat-hf': {
                'context_window': 4096,
                'training_cutoff': '2023-07',
                'strengths': ['Chat optimized', 'Open source', 'Safety focused'],
                'use_cases': ['Conversational AI', 'Q&A', 'Assistant applications'],
                'fine_tuning_strategy': 'RLHF for helpfulness and safety',
                'instruction_following': 'Very good',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'meta-llama/Llama-2-13b-chat-hf': {
                'context_window': 4096,
                'training_cutoff': '2023-07',
                'strengths': ['Larger model', 'Better performance', 'Chat optimized'],
                'use_cases': ['Advanced chat', 'Complex reasoning', 'Content creation'],
                'fine_tuning_strategy': 'RLHF for helpfulness and safety',
                'instruction_following': 'Excellent',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'mistralai/Mistral-7B-v0.1': {
                'context_window': 32768,
                'training_cutoff': '2023-09',
                'strengths': ['Large context', 'Efficient', 'Open source'],
                'use_cases': ['Long document processing', 'Code analysis'],
                'fine_tuning_strategy': 'Standard pre-training',
                'instruction_following': 'Basic',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'mistralai/Mistral-7B-Instruct-v0.1': {
                'context_window': 32768,
                'training_cutoff': '2023-09',
                'strengths': ['Instruction following', 'Large context', 'Efficient'],
                'use_cases': ['Task completion', 'Q&A', 'Analysis'],
                'fine_tuning_strategy': 'Instruction fine-tuning',
                'instruction_following': 'Very good',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'codellama/CodeLlama-7b-Python-hf': {
                'context_window': 16384,
                'training_cutoff': '2023-07',
                'strengths': ['Python specialized', 'Code understanding', 'Open source'],
                'use_cases': ['Python code generation', 'Code completion', 'Debugging'],
                'fine_tuning_strategy': 'Code-specific fine-tuning on Python',
                'instruction_following': 'Good (code-focused)',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'codellama/CodeLlama-7b-Instruct-hf': {
                'context_window': 16384,
                'training_cutoff': '2023-07',
                'strengths': ['Code instruction following', 'Multi-language', 'Open source'],
                'use_cases': ['Code generation', 'Code explanation', 'Programming help'],
                'fine_tuning_strategy': 'Code + instruction fine-tuning',
                'instruction_following': 'Very good (code tasks)',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            },
            'HuggingFaceH4/zephyr-7b-beta': {
                'context_window': 32768,
                'training_cutoff': '2023-10',
                'strengths': ['Chat optimized', 'DPO training', 'Open source'],
                'use_cases': ['Conversational AI', 'Helpful assistant', 'Q&A'],
                'fine_tuning_strategy': 'DPO (Direct Preference Optimization)',
                'instruction_following': 'Excellent',
                'cost_per_1k_tokens': 'Free (self-hosted)'
            }
        }
        
        return characteristics.get(model_name, {
            'context_window': 4096,
            'training_cutoff': 'Unknown',
            'strengths': ['Open source', 'Customizable'],
            'use_cases': ['General tasks', 'Research'],
            'fine_tuning_strategy': 'Standard',
            'instruction_following': 'Variable',
            'cost_per_1k_tokens': 'Free (self-hosted)'
        })
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens for Hugging Face models."""
        try:
            # Try to use transformers tokenizer if available
            from transformers import AutoTokenizer
            
            # Use a compatible tokenizer
            if 'llama' in model_name.lower():
                tokenizer_name = 'meta-llama/Llama-2-7b-hf'
            elif 'mistral' in model_name.lower():
                tokenizer_name = 'mistralai/Mistral-7B-v0.1'
            elif 'codellama' in model_name.lower():
                tokenizer_name = 'codellama/CodeLlama-7b-hf'
            else:
                # Fallback tokenizer
                tokenizer_name = 'gpt2'
            
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
            return len(tokenizer.encode(text))
            
        except (ImportError, Exception):
            # Fallback to word-based estimation
            return len(text.split()) * 1.3
    
    def get_context_window(self, model_name: str) -> int:
        """Get context window size for Hugging Face models."""
        windows = {
            'meta-llama/Llama-2-7b-hf': 4096,
            'meta-llama/Llama-2-7b-chat-hf': 4096,
            'meta-llama/Llama-2-13b-hf': 4096,
            'meta-llama/Llama-2-13b-chat-hf': 4096,
            'mistralai/Mistral-7B-v0.1': 32768,
            'mistralai/Mistral-7B-Instruct-v0.1': 32768,
            'codellama/CodeLlama-7b-Python-hf': 16384,
            'codellama/CodeLlama-7b-Instruct-hf': 16384,
            'HuggingFaceH4/zephyr-7b-beta': 32768,
            'openchat/openchat-3.5-1210': 8192,
        }
        return windows.get(model_name, 4096)
    
    def get_default_model(self, model_type: str) -> str:
        """Get default Hugging Face model for type."""
        defaults = {
            'base': 'meta-llama/Llama-2-7b-hf',
            'instruct': 'meta-llama/Llama-2-7b-chat-hf',
            'fine-tuned': 'codellama/CodeLlama-7b-Python-hf'
        }
        return defaults.get(model_type)
    
    def validate_api_key(self) -> bool:
        """Validate Hugging Face API key."""
        return self.api_key is not None and len(self.api_key.strip()) > 0
