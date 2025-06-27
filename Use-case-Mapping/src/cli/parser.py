"""
Command-line argument parser for the model comparison tool.
"""

import argparse
from typing import Optional


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Model Comparison and Use-case Mapping Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "Explain quantum computing" --provider openai --model-type instruct
  %(prog)s --query "Write a Python function" --compare-all --visualize
  %(prog)s --interactive
  %(prog)s --query "Explain ML" --provider anthropic --save results.json
        """
    )
    
    # Main query argument
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Input query for the models'
    )
    
    # Provider selection
    parser.add_argument(
        '--provider', '-p',
        choices=['openai', 'anthropic', 'huggingface'],
        default='openai',
        help='Choose AI provider (default: openai)'
    )
    
    # Model type selection
    parser.add_argument(
        '--model-type', '-t',
        choices=['base', 'instruct', 'fine-tuned'],
        default='instruct',
        help='Model type to use (default: instruct)'
    )
    
    # Specific model name
    parser.add_argument(
        '--model', '-m',
        type=str,
        help='Specific model name (overrides model-type selection)'
    )
    
    # Comparison mode
    parser.add_argument(
        '--compare-all', '-c',
        action='store_true',
        help='Compare across all available models'
    )
    
    # Interactive mode
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start interactive mode'
    )
    
    # Visualization
    parser.add_argument(
        '--visualize', '-v',
        action='store_true',
        help='Show token usage and context window visualization'
    )
    
    # Output format
    parser.add_argument(
        '--output', '-o',
        choices=['console', 'json', 'markdown'],
        default='console',
        help='Output format (default: console)'
    )
    
    # Save results
    parser.add_argument(
        '--save', '-s',
        type=str,
        help='Save results to file (specify filename)'
    )
    
    # Model parameters
    model_group = parser.add_argument_group('model parameters')
    model_group.add_argument(
        '--max-tokens',
        type=int,
        default=1000,
        help='Maximum tokens for response (default: 1000)'
    )
    
    model_group.add_argument(
        '--temperature',
        type=float,
        default=0.7,
        help='Temperature for response generation (default: 0.7)'
    )
    
    model_group.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    
    # Logging and debug
    debug_group = parser.add_argument_group('debugging')
    debug_group.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    debug_group.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with detailed error messages'
    )
    
    debug_group.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Configuration
    config_group = parser.add_argument_group('configuration')
    config_group.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    config_group.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable response caching'
    )
    
    return parser


def validate_args(args: argparse.Namespace) -> Optional[str]:
    """
    Validate command-line arguments and return error message if invalid.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Error message if validation fails, None if valid
    """
    # Check if query is provided when not in interactive mode
    if not args.interactive and not args.query:
        return "Query is required when not in interactive mode. Use --query or --interactive."
    
    # Validate temperature range
    if not 0.0 <= args.temperature <= 2.0:
        return "Temperature must be between 0.0 and 2.0"
    
    # Validate max_tokens
    if args.max_tokens <= 0:
        return "Max tokens must be greater than 0"
    
    # Validate timeout
    if args.timeout <= 0:
        return "Timeout must be greater than 0"
    
    # Check for conflicting options
    if args.compare_all and args.model:
        return "Cannot use --compare-all with specific --model selection"
    
    return None
