"""
Basic tests for the model comparison tool.
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.model_config import load_config, validate_config
from utils.tokenizer import TokenizerUtils
from providers.provider_factory import ProviderFactory


class TestModelConfig:
    """Test model configuration functionality."""
    
    def test_load_config(self):
        """Test loading configuration."""
        config = load_config()
        assert isinstance(config, dict)
        assert 'max_tokens' in config
        assert 'temperature' in config
        assert 'models' in config
    
    def test_validate_config(self):
        """Test configuration validation."""
        valid_config = {
            'max_tokens': 1000,
            'temperature': 0.7,
            'timeout': 30,
            'log_level': 'INFO'
        }
        issues = validate_config(valid_config)
        # Should have warnings about missing API keys but no errors about parameters
        assert all('Error:' not in issue for issue in issues if 'API key' not in issue)
        
        invalid_config = {
            'max_tokens': -1,
            'temperature': 3.0,
            'timeout': -5
        }
        issues = validate_config(invalid_config)
        assert any('max_tokens must be greater than 0' in issue for issue in issues)
        assert any('temperature must be between 0.0 and 2.0' in issue for issue in issues)


class TestTokenizer:
    """Test tokenization utilities."""
    
    def test_basic_token_estimate(self):
        """Test basic token estimation."""
        text = "Hello world this is a test"
        tokens = TokenizerUtils._basic_token_estimate(text)
        assert tokens > 0
        assert isinstance(tokens, int)
    
    def test_analyze_text(self):
        """Test text analysis."""
        text = "Hello world! This is a test. How are you?"
        analysis = TokenizerUtils.analyze_text(text)
        
        assert 'characters' in analysis
        assert 'words' in analysis
        assert 'sentences' in analysis
        assert analysis['words'] > 0
        assert analysis['sentences'] > 0
    
    def test_count_functions(self):
        """Test individual counting functions."""
        text = "Hello world! This is a test."
        
        assert TokenizerUtils.count_words(text) == 6
        assert TokenizerUtils.count_characters(text) == len(text)
        assert TokenizerUtils.count_sentences(text) == 2


class TestProviderFactory:
    """Test provider factory functionality."""
    
    def test_provider_factory_creation(self):
        """Test creating provider factory."""
        config = {'openai_api_key': 'test_key'}
        factory = ProviderFactory(config)
        assert factory.config == config
    
    def test_get_available_providers(self):
        """Test getting available providers."""
        config = {
            'openai_api_key': 'test_key',
            'anthropic_api_key': 'test_key'
        }
        factory = ProviderFactory(config)
        providers = factory.get_available_providers()
        
        assert 'openai' in providers
        assert 'anthropic' in providers
    
    def test_validate_provider_config(self):
        """Test provider configuration validation."""
        config = {}
        factory = ProviderFactory(config)
        
        # Should return False for missing API keys
        assert not factory.validate_provider_config('openai')


if __name__ == '__main__':
    pytest.main([__file__])
