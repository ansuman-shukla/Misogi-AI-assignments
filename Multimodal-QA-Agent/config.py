"""
Configuration settings for the Multimodal QA Agent.
"""

import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ModelConfig:
    """Configuration for AI models."""
    vision_model: str = "gemini-pro-vision"
    text_model: str = "gemini-pro"
    temperature: float = 0.3
    max_tokens: int = 1000

@dataclass
class ImageConfig:
    """Configuration for image processing."""
    max_image_size: int = 1024
    supported_formats: List[str] = None
    max_file_size_mb: int = 10
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']

@dataclass
class AppConfig:
    """Main application configuration."""
    app_title: str = "Multimodal QA Agent"
    app_icon: str = "🤖"
    max_history: int = 50
    enable_logging: bool = True
    log_level: str = "INFO"

class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.model = ModelConfig()
        self.image = ImageConfig()
        self.app = AppConfig()
        
        # Load environment variables
        self._load_env_vars()
    
    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # API Keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Model settings
        if os.getenv("VISION_MODEL"):
            self.model.vision_model = os.getenv("VISION_MODEL")
        if os.getenv("TEXT_MODEL"):
            self.model.text_model = os.getenv("TEXT_MODEL")
        if os.getenv("MODEL_TEMPERATURE"):
            self.model.temperature = float(os.getenv("MODEL_TEMPERATURE"))
        
        # Image settings
        if os.getenv("MAX_IMAGE_SIZE"):
            self.image.max_image_size = int(os.getenv("MAX_IMAGE_SIZE"))
        if os.getenv("MAX_FILE_SIZE_MB"):
            self.image.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB"))
        
        # App settings
        if os.getenv("APP_TITLE"):
            self.app.app_title = os.getenv("APP_TITLE")
        if os.getenv("ENABLE_LOGGING"):
            self.app.enable_logging = os.getenv("ENABLE_LOGGING").lower() == "true"
    
    def validate(self) -> List[str]:
        """
        Validate the configuration.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        if not self.google_api_key:
            errors.append("GOOGLE_API_KEY is required")
        
        if self.model.temperature < 0 or self.model.temperature > 1:
            errors.append("Model temperature must be between 0 and 1")
        
        if self.image.max_image_size <= 0:
            errors.append("Max image size must be positive")
        
        if self.image.max_file_size_mb <= 0:
            errors.append("Max file size must be positive")
        
        return errors
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {
            'model': {
                'vision_model': self.model.vision_model,
                'text_model': self.model.text_model,
                'temperature': self.model.temperature,
                'max_tokens': self.model.max_tokens
            },
            'image': {
                'max_image_size': self.image.max_image_size,
                'supported_formats': self.image.supported_formats,
                'max_file_size_mb': self.image.max_file_size_mb
            },
            'app': {
                'app_title': self.app.app_title,
                'app_icon': self.app.app_icon,
                'max_history': self.app.max_history,
                'enable_logging': self.app.enable_logging,
                'log_level': self.app.log_level
            }
        }

# Default configuration instance
config = Config()
