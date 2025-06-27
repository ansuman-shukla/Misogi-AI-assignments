"""
Model configuration and settings management.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from environment variables and config files.
    
    Args:
        config_path: Path to configuration file (optional)
        
    Returns:
        Configuration dictionary
    """
    # Load environment variables
    load_dotenv()
    
    # Default configuration
    config = {
        # API Keys
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        'huggingface_api_key': os.getenv('HUGGINGFACE_API_KEY'),
        
        # API Endpoints
        'openai_base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        'anthropic_base_url': os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com'),
        'huggingface_base_url': os.getenv('HUGGINGFACE_BASE_URL', 'https://api-inference.huggingface.co'),
        
        # Model Parameters
        'max_tokens': int(os.getenv('DEFAULT_MAX_TOKENS', 1000)),
        'temperature': float(os.getenv('DEFAULT_TEMPERATURE', 0.7)),
        'timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),
        
        # Logging
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('LOG_FILE', 'model_comparisons.log'),
        
        # Visualization
        'enable_visualization': os.getenv('ENABLE_VISUALIZATION', 'true').lower() == 'true',
        'chart_theme': os.getenv('CHART_THEME', 'dark'),
        
        # Caching
        'enable_cache': True,
        'cache_duration': 3600,  # 1 hour
        
        # Rate Limiting
        'rate_limit_per_minute': 60,
        'rate_limit_per_hour': 1000,
    }
    
    # Load from YAML config file if provided
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    # Load default models config
    config['models'] = load_models_config()
    
    return config


def load_models_config() -> Dict[str, Any]:
    """
    Load models configuration.
    
    Returns:
        Models configuration dictionary
    """
    return {
        'openai': {
            'base': {
                'default': 'gpt-3.5-turbo-instruct',
                'models': [
                    'gpt-3.5-turbo-instruct',
                    'text-davinci-003'
                ]
            },
            'instruct': {
                'default': 'gpt-3.5-turbo',
                'models': [
                    'gpt-3.5-turbo',
                    'gpt-3.5-turbo-16k',
                    'gpt-4',
                    'gpt-4-turbo',
                    'gpt-4o',
                    'gpt-4o-mini'
                ]
            },
            'fine-tuned': {
                'default': None,
                'models': []
            }
        },
        'anthropic': {
            'base': {
                'default': None,
                'models': []
            },
            'instruct': {
                'default': 'claude-3-sonnet-20240229',
                'models': [
                    'claude-3-haiku-20240307',
                    'claude-3-sonnet-20240229',
                    'claude-3-opus-20240229',
                    'claude-3-5-sonnet-20240620',
                    'claude-2.1',
                    'claude-instant-1.2'
                ]
            },
            'fine-tuned': {
                'default': None,
                'models': []
            }
        },
        'huggingface': {
            'base': {
                'default': 'meta-llama/Llama-2-7b-hf',
                'models': [
                    'meta-llama/Llama-2-7b-hf',
                    'meta-llama/Llama-2-13b-hf',
                    'mistralai/Mistral-7B-v0.1',
                    'EleutherAI/gpt-neo-2.7B'
                ]
            },
            'instruct': {
                'default': 'meta-llama/Llama-2-7b-chat-hf',
                'models': [
                    'meta-llama/Llama-2-7b-chat-hf',
                    'meta-llama/Llama-2-13b-chat-hf',
                    'mistralai/Mistral-7B-Instruct-v0.1',
                    'HuggingFaceH4/zephyr-7b-beta',
                    'openchat/openchat-3.5-1210'
                ]
            },
            'fine-tuned': {
                'default': 'codellama/CodeLlama-7b-Python-hf',
                'models': [
                    'codellama/CodeLlama-7b-Python-hf',
                    'codellama/CodeLlama-7b-Instruct-hf',
                    'WizardLM/WizardCoder-15B-V1.0',
                    'Salesforce/codegen-2B-Python'
                ]
            }
        }
    }


def save_config(config: Dict[str, Any], config_path: str):
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    try:
        # Remove sensitive data before saving
        safe_config = config.copy()
        sensitive_keys = ['openai_api_key', 'anthropic_api_key', 'huggingface_api_key']
        for key in sensitive_keys:
            if key in safe_config:
                safe_config[key] = '***'
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(safe_config, f, default_flow_style=False, indent=2)
            
    except Exception as e:
        print(f"Error saving config: {e}")


def validate_config(config: Dict[str, Any]) -> list[str]:
    """
    Validate configuration and return list of issues.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of validation error messages
    """
    issues = []
    
    # Check API keys
    api_keys = {
        'openai_api_key': 'OpenAI',
        'anthropic_api_key': 'Anthropic',
        'huggingface_api_key': 'Hugging Face'
    }
    
    has_any_key = False
    for key, provider in api_keys.items():
        if config.get(key):
            has_any_key = True
        else:
            issues.append(f"Warning: {provider} API key not configured")
    
    if not has_any_key:
        issues.append("Error: No API keys configured. At least one provider API key is required.")
    
    # Check numeric parameters
    if config.get('max_tokens', 0) <= 0:
        issues.append("Error: max_tokens must be greater than 0")
    
    if not 0 <= config.get('temperature', 0.7) <= 2.0:
        issues.append("Error: temperature must be between 0.0 and 2.0")
    
    if config.get('timeout', 30) <= 0:
        issues.append("Error: timeout must be greater than 0")
    
    # Check log level
    valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    if config.get('log_level', 'INFO').upper() not in valid_log_levels:
        issues.append(f"Warning: Invalid log level. Must be one of: {valid_log_levels}")
    
    return issues


def get_default_config_path() -> str:
    """
    Get default configuration file path.
    
    Returns:
        Default config file path
    """
    return os.path.join(os.getcwd(), 'config', 'settings.yaml')


def create_default_config_file():
    """Create default configuration file."""
    config_dir = os.path.join(os.getcwd(), 'config')
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, 'settings.yaml')
    
    if not os.path.exists(config_path):
        default_config = {
            'api_keys': {
                'openai_api_key': 'your_openai_api_key_here',
                'anthropic_api_key': 'your_anthropic_api_key_here',
                'huggingface_api_key': 'your_huggingface_api_key_here'
            },
            'model_parameters': {
                'max_tokens': 1000,
                'temperature': 0.7,
                'timeout': 30
            },
            'logging': {
                'log_level': 'INFO',
                'log_file': 'model_comparisons.log'
            },
            'visualization': {
                'enable_visualization': True,
                'chart_theme': 'dark'
            }
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, indent=2)
            print(f"Created default configuration file: {config_path}")
        except Exception as e:
            print(f"Error creating config file: {e}")


class ConfigManager:
    """Configuration manager class."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = load_config(config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values."""
        self.config.update(updates)
    
    def save(self, path: Optional[str] = None):
        """Save configuration to file."""
        save_path = path or self.config_path or get_default_config_path()
        save_config(self.config, save_path)
    
    def validate(self) -> list[str]:
        """Validate current configuration."""
        return validate_config(self.config)
    
    def reload(self):
        """Reload configuration from file."""
        self.config = load_config(self.config_path)
