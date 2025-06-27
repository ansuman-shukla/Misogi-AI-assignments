"""
Provider factory for creating model provider instances.
"""

from typing import Dict, Any, Optional
import os
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .huggingface_provider import HuggingFaceProvider


class ProviderFactory:
    """Factory class for creating model provider instances."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._providers = {}
    
    def get_provider(self, provider_name: str):
        """
        Get or create a provider instance.
        
        Args:
            provider_name: Name of the provider ('openai', 'anthropic', 'huggingface')
            
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider is not supported or not configured
        """
        if provider_name in self._providers:
            return self._providers[provider_name]
        
        provider_name = provider_name.lower()
        
        if provider_name == 'openai':
            provider = self._create_openai_provider()
        elif provider_name == 'anthropic':
            provider = self._create_anthropic_provider()
        elif provider_name == 'huggingface':
            provider = self._create_huggingface_provider()
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        self._providers[provider_name] = provider
        return provider
    
    def _create_openai_provider(self) -> OpenAIProvider:
        """Create OpenAI provider instance."""
        api_key = self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or provide in config.")
        
        return OpenAIProvider(self.config)
    
    def _create_anthropic_provider(self) -> AnthropicProvider:
        """Create Anthropic provider instance."""
        api_key = self.config.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or provide in config.")
        
        return AnthropicProvider(self.config)
    
    def _create_huggingface_provider(self) -> HuggingFaceProvider:
        """Create Hugging Face provider instance."""
        api_key = self.config.get('huggingface_api_key') or os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            raise ValueError("Hugging Face API key not found. Set HUGGINGFACE_API_KEY environment variable or provide in config.")
        
        return HuggingFaceProvider(self.config)
    
    def get_available_providers(self) -> list[str]:
        """
        Get list of available providers based on configured API keys.
        
        Returns:
            List of available provider names
        """
        available = []
        
        # Check OpenAI
        if self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY'):
            available.append('openai')
        
        # Check Anthropic
        if self.config.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY'):
            available.append('anthropic')
        
        # Check Hugging Face
        if self.config.get('huggingface_api_key') or os.getenv('HUGGINGFACE_API_KEY'):
            available.append('huggingface')
        
        return available
    
    def validate_provider_config(self, provider_name: str) -> bool:
        """
        Validate configuration for a specific provider.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            True if configuration is valid
        """
        try:
            provider = self.get_provider(provider_name)
            return provider.validate_api_key()
        except Exception:
            return False
    
    def get_all_available_models(self) -> Dict[str, Dict[str, list]]:
        """
        Get all available models from all configured providers.
        
        Returns:
            Dictionary mapping provider names to their available models
        """
        all_models = {}
        
        for provider_name in self.get_available_providers():
            try:
                provider = self.get_provider(provider_name)
                all_models[provider_name] = provider.get_available_models()
            except Exception as e:
                # Skip providers that can't be initialized
                continue
        
        return all_models
