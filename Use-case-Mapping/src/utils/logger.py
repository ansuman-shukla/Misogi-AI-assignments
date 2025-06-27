"""
Logging configuration and utilities.
"""

import logging
import os
from typing import Optional
from datetime import datetime


def setup_logger(
    level: str = 'INFO',
    log_file: Optional[str] = None,
    logger_name: str = 'model_comparison'
) -> logging.Logger:
    """
    Setup logger with console and file handlers.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
        logger_name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)  # Log everything to file
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            logger.warning(f"Could not create file handler: {e}")
    
    return logger


def log_model_request(
    logger: logging.Logger,
    provider: str,
    model_name: str,
    query: str,
    start_time: float
):
    """
    Log model request details.
    
    Args:
        logger: Logger instance
        provider: Provider name
        model_name: Model name
        query: Input query
        start_time: Request start time
    """
    logger.info(
        f"Model Request - Provider: {provider}, Model: {model_name}, "
        f"Query length: {len(query)} chars, Started: {datetime.fromtimestamp(start_time)}"
    )


def log_model_response(
    logger: logging.Logger,
    provider: str,
    model_name: str,
    response_length: int,
    token_usage: dict,
    response_time: float,
    success: bool = True,
    error: Optional[str] = None
):
    """
    Log model response details.
    
    Args:
        logger: Logger instance
        provider: Provider name
        model_name: Model name
        response_length: Length of response
        token_usage: Token usage information
        response_time: Response time in seconds
        success: Whether request was successful
        error: Error message if failed
    """
    status = "SUCCESS" if success else "ERROR"
    
    log_msg = (
        f"Model Response - Provider: {provider}, Model: {model_name}, "
        f"Status: {status}, Response length: {response_length} chars, "
        f"Tokens: {token_usage.get('total_tokens', 'N/A')}, "
        f"Time: {response_time:.2f}s"
    )
    
    if error:
        log_msg += f", Error: {error}"
    
    if success:
        logger.info(log_msg)
    else:
        logger.error(log_msg)


def log_comparison_start(
    logger: logging.Logger,
    query: str,
    providers: list,
    model_types: list
):
    """
    Log start of model comparison.
    
    Args:
        logger: Logger instance
        query: Input query
        providers: List of providers
        model_types: List of model types
    """
    logger.info(
        f"Comparison Started - Query: '{query[:50]}...', "
        f"Providers: {providers}, Model Types: {model_types}"
    )


def log_comparison_complete(
    logger: logging.Logger,
    total_responses: int,
    successful_responses: int,
    total_time: float
):
    """
    Log completion of model comparison.
    
    Args:
        logger: Logger instance
        total_responses: Total responses attempted
        successful_responses: Number of successful responses
        total_time: Total time taken
    """
    logger.info(
        f"Comparison Complete - Total: {total_responses}, "
        f"Successful: {successful_responses}, Total Time: {total_time:.2f}s"
    )


class ModelComparisonLogger:
    """Context manager for logging model comparisons."""
    
    def __init__(self, logger: logging.Logger, query: str):
        self.logger = logger
        self.query = query
        self.start_time = None
        self.responses = []
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        self.logger.info(f"Starting model comparison for query: '{self.query[:50]}...'")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        total_time = time.time() - self.start_time
        successful = len([r for r in self.responses if not r.get('error')])
        
        log_comparison_complete(
            self.logger,
            len(self.responses),
            successful,
            total_time
        )
        
        if exc_type:
            self.logger.error(f"Comparison failed with error: {exc_val}")
    
    def add_response(self, response: dict):
        """Add a response to the logger."""
        self.responses.append(response)
        
        log_model_response(
            self.logger,
            response.get('provider', 'Unknown'),
            response.get('model_name', 'Unknown'),
            len(response.get('response', '')),
            response.get('token_usage', {}),
            response.get('response_time', 0),
            success=not response.get('error'),
            error=response.get('error')
        )
