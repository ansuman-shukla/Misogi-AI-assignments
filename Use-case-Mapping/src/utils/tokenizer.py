"""
Tokenization utilities for different model providers.
"""

from typing import Dict, Any, Optional
import re


class TokenizerUtils:
    """Utility class for tokenization across different providers."""
    
    @staticmethod
    def estimate_tokens(text: str, provider: str = 'openai', model_name: str = '') -> int:
        """
        Estimate token count for a given text and provider.
        
        Args:
            text: Text to tokenize
            provider: Provider name (openai, anthropic, huggingface)
            model_name: Specific model name
            
        Returns:
            Estimated token count
        """
        if provider.lower() == 'openai':
            return TokenizerUtils._estimate_openai_tokens(text, model_name)
        elif provider.lower() == 'anthropic':
            return TokenizerUtils._estimate_anthropic_tokens(text, model_name)
        elif provider.lower() == 'huggingface':
            return TokenizerUtils._estimate_huggingface_tokens(text, model_name)
        else:
            return TokenizerUtils._basic_token_estimate(text)
    
    @staticmethod
    def _estimate_openai_tokens(text: str, model_name: str = '') -> int:
        """Estimate tokens for OpenAI models."""
        try:
            import tiktoken
            
            # Select appropriate encoding
            if 'gpt-4' in model_name.lower():
                encoding = tiktoken.encoding_for_model("gpt-4")
            elif 'gpt-3.5' in model_name.lower():
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            else:
                encoding = tiktoken.get_encoding("cl100k_base")
            
            return len(encoding.encode(text))
            
        except ImportError:
            # Fallback if tiktoken not available
            return TokenizerUtils._basic_token_estimate(text)
        except Exception:
            return TokenizerUtils._basic_token_estimate(text)
    
    @staticmethod
    def _estimate_anthropic_tokens(text: str, model_name: str = '') -> int:
        """Estimate tokens for Anthropic models."""
        try:
            # Anthropic uses similar tokenization to OpenAI
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except ImportError:
            return TokenizerUtils._basic_token_estimate(text)
        except Exception:
            return TokenizerUtils._basic_token_estimate(text)
    
    @staticmethod
    def _estimate_huggingface_tokens(text: str, model_name: str = '') -> int:
        """Estimate tokens for Hugging Face models."""
        try:
            from transformers import AutoTokenizer
            
            # Select appropriate tokenizer
            if 'llama' in model_name.lower():
                tokenizer_name = 'meta-llama/Llama-2-7b-hf'
            elif 'mistral' in model_name.lower():
                tokenizer_name = 'mistralai/Mistral-7B-v0.1'
            elif 'codellama' in model_name.lower():
                tokenizer_name = 'codellama/CodeLlama-7b-hf'
            else:
                tokenizer_name = 'gpt2'
            
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
            return len(tokenizer.encode(text))
            
        except ImportError:
            return TokenizerUtils._basic_token_estimate(text)
        except Exception:
            return TokenizerUtils._basic_token_estimate(text)
    
    @staticmethod
    def _basic_token_estimate(text: str) -> int:
        """
        Basic token estimation using word count.
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count (words * 1.3)
        """
        # Simple word-based estimation
        # Typical ratio is about 1.3 tokens per word for English
        words = len(text.split())
        return int(words * 1.3)
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    @staticmethod
    def count_characters(text: str) -> int:
        """Count characters in text."""
        return len(text)
    
    @staticmethod
    def count_sentences(text: str) -> int:
        """Count sentences in text."""
        # Simple sentence counting using punctuation
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])
    
    @staticmethod
    def analyze_text(text: str) -> Dict[str, Any]:
        """
        Comprehensive text analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with text statistics
        """
        return {
            'characters': TokenizerUtils.count_characters(text),
            'words': TokenizerUtils.count_words(text),
            'sentences': TokenizerUtils.count_sentences(text),
            'estimated_tokens_openai': TokenizerUtils.estimate_tokens(text, 'openai'),
            'estimated_tokens_anthropic': TokenizerUtils.estimate_tokens(text, 'anthropic'),
            'estimated_tokens_basic': TokenizerUtils._basic_token_estimate(text),
            'avg_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1),
            'avg_sentence_length': TokenizerUtils.count_words(text) / max(TokenizerUtils.count_sentences(text), 1)
        }
    
    @staticmethod
    def check_context_window(text: str, context_window: int, provider: str = 'openai', model_name: str = '') -> Dict[str, Any]:
        """
        Check if text fits within context window.
        
        Args:
            text: Text to check
            context_window: Maximum context window size
            provider: Provider name
            model_name: Model name
            
        Returns:
            Dictionary with context analysis
        """
        estimated_tokens = TokenizerUtils.estimate_tokens(text, provider, model_name)
        
        return {
            'estimated_tokens': estimated_tokens,
            'context_window': context_window,
            'fits_in_window': estimated_tokens <= context_window,
            'utilization_percentage': (estimated_tokens / context_window) * 100 if context_window > 0 else 0,
            'remaining_tokens': max(0, context_window - estimated_tokens)
        }
    
    @staticmethod
    def truncate_to_tokens(text: str, max_tokens: int, provider: str = 'openai', model_name: str = '') -> str:
        """
        Truncate text to fit within token limit.
        
        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens
            provider: Provider name
            model_name: Model name
            
        Returns:
            Truncated text
        """
        current_tokens = TokenizerUtils.estimate_tokens(text, provider, model_name)
        
        if current_tokens <= max_tokens:
            return text
        
        # Binary search to find optimal truncation point
        words = text.split()
        left, right = 0, len(words)
        
        while left < right:
            mid = (left + right + 1) // 2
            truncated = ' '.join(words[:mid])
            
            if TokenizerUtils.estimate_tokens(truncated, provider, model_name) <= max_tokens:
                left = mid
            else:
                right = mid - 1
        
        return ' '.join(words[:left])
    
    @staticmethod
    def optimize_prompt_length(
        prompt: str, 
        max_prompt_tokens: int, 
        max_response_tokens: int,
        context_window: int,
        provider: str = 'openai',
        model_name: str = ''
    ) -> Dict[str, Any]:
        """
        Optimize prompt length to fit within context window while reserving space for response.
        
        Args:
            prompt: Original prompt
            max_prompt_tokens: Maximum tokens for prompt
            max_response_tokens: Expected response tokens
            context_window: Total context window
            provider: Provider name
            model_name: Model name
            
        Returns:
            Dictionary with optimization results
        """
        # Calculate available tokens for prompt
        available_for_prompt = min(max_prompt_tokens, context_window - max_response_tokens - 100)  # 100 token buffer
        
        prompt_tokens = TokenizerUtils.estimate_tokens(prompt, provider, model_name)
        
        if prompt_tokens <= available_for_prompt:
            return {
                'original_prompt': prompt,
                'optimized_prompt': prompt,
                'original_tokens': prompt_tokens,
                'optimized_tokens': prompt_tokens,
                'truncated': False,
                'available_tokens': available_for_prompt,
                'response_space': context_window - prompt_tokens
            }
        
        # Truncate prompt
        optimized_prompt = TokenizerUtils.truncate_to_tokens(prompt, available_for_prompt, provider, model_name)
        optimized_tokens = TokenizerUtils.estimate_tokens(optimized_prompt, provider, model_name)
        
        return {
            'original_prompt': prompt,
            'optimized_prompt': optimized_prompt,
            'original_tokens': prompt_tokens,
            'optimized_tokens': optimized_tokens,
            'truncated': True,
            'available_tokens': available_for_prompt,
            'response_space': context_window - optimized_tokens,
            'truncation_ratio': len(optimized_prompt) / len(prompt)
        }
