#!/usr/bin/env python3
"""
Model Comparison and Use-case Mapping Tool
Main entry point for the CLI application.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Check for required dependencies
def check_dependencies():
    """Check if required dependencies are installed."""
    missing_deps = []
    
    try:
        import rich
    except ImportError:
        missing_deps.append("rich")
    
    try:
        import openai
    except ImportError:
        missing_deps.append("openai")
    
    try:
        import anthropic
    except ImportError:
        missing_deps.append("anthropic")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nPlease install dependencies with:")
        print("   pip install -r requirements.txt")
        print("\nOr run setup script:")
        print("   python setup.py")
        return False
    
    return True

if not check_dependencies():
    sys.exit(1)

# Now import our modules
try:
    from cli.parser import create_parser
    from cli.interactive import InteractiveMode
    from utils.logger import setup_logger
    from models.model_config import load_config
    from providers.provider_factory import ProviderFactory
    from utils.visualization import ModelVisualizer
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run: python setup.py")
    sys.exit(1)


async def main():
    """Main application entry point."""
    console = Console()
    
    try:
        # Parse command line arguments
        parser = create_parser()
        args = parser.parse_args()
        
        # Setup logging
        logger = setup_logger(args.log_level if hasattr(args, 'log_level') else 'INFO')
        
        # Load configuration
        config = load_config()
        
        # Handle interactive mode
        if getattr(args, 'interactive', False):
            interactive = InteractiveMode(console, config)
            await interactive.run()
            return
        
        # Validate required arguments for non-interactive mode
        if not hasattr(args, 'query') or not args.query:
            console.print("[red]Error: Query is required in non-interactive mode[/red]")
            console.print("Use --interactive for interactive mode or provide --query")
            return
        
        # Initialize provider factory
        provider_factory = ProviderFactory(config)
        
        # Handle compare-all mode
        if getattr(args, 'compare_all', False):
            await compare_all_models(args.query, provider_factory, console, args)
        else:
            # Single model query
            await single_model_query(args, provider_factory, console)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if hasattr(args, 'debug') and args.debug:
            import traceback
            console.print(traceback.format_exc())


async def single_model_query(args, provider_factory, console):
    """Handle single model query."""
    try:
        # Get provider
        provider_name = getattr(args, 'provider', 'openai')
        model_type = getattr(args, 'model_type', 'instruct')
        model_name = getattr(args, 'model', None)
        
        provider = provider_factory.get_provider(provider_name)
        
        # Generate response
        with console.status(f"[bold green]Querying {provider_name} model..."):
            response = await provider.generate_response(
                query=args.query,
                model_type=model_type,
                model_name=model_name
            )
        
        # Display results
        display_single_result(response, console, args)
        
        # Visualization if requested
        if getattr(args, 'visualize', False):
            visualizer = ModelVisualizer()
            visualizer.visualize_single_response(response)
            
    except Exception as e:
        console.print(f"[red]Error in single model query: {str(e)}[/red]")


async def compare_all_models(query, provider_factory, console, args):
    """Compare response across all available models."""
    console.print(f"[bold blue]Comparing models for query:[/bold blue] {query}")
    console.print()
    
    providers = ['openai', 'anthropic', 'huggingface']
    model_types = ['base', 'instruct', 'fine-tuned']
    
    results = []
    
    for provider_name in providers:
        try:
            provider = provider_factory.get_provider(provider_name)
            
            for model_type in model_types:
                try:
                    with console.status(f"[bold green]Querying {provider_name} {model_type} model..."):
                        response = await provider.generate_response(
                            query=query,
                            model_type=model_type
                        )
                        results.append(response)
                        
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to query {provider_name} {model_type}: {str(e)}[/yellow]")
                    
        except Exception as e:
            console.print(f"[yellow]Warning: Provider {provider_name} unavailable: {str(e)}[/yellow]")
    
    # Display comparison results
    display_comparison_results(results, console, args)
    
    # Visualization if requested
    if getattr(args, 'visualize', False):
        visualizer = ModelVisualizer()
        visualizer.visualize_comparison(results)


def display_single_result(response, console, args):
    """Display single model response."""
    console.print(f"[bold cyan]Model:[/bold cyan] {response.get('model_name', 'Unknown')}")
    console.print(f"[bold cyan]Provider:[/bold cyan] {response.get('provider', 'Unknown')}")
    console.print(f"[bold cyan]Type:[/bold cyan] {response.get('model_type', 'Unknown')}")
    console.print()
    
    console.print("[bold green]Response:[/bold green]")
    console.print(response.get('response', 'No response'))
    console.print()
    
    # Model characteristics
    if 'characteristics' in response:
        console.print("[bold yellow]Model Characteristics:[/bold yellow]")
        for key, value in response['characteristics'].items():
            console.print(f"  • {key}: {value}")
        console.print()
    
    # Token usage
    if 'token_usage' in response:
        usage = response['token_usage']
        console.print("[bold magenta]Token Usage:[/bold magenta]")
        console.print(f"  • Input tokens: {usage.get('input_tokens', 'N/A')}")
        console.print(f"  • Output tokens: {usage.get('output_tokens', 'N/A')}")
        console.print(f"  • Total tokens: {usage.get('total_tokens', 'N/A')}")
        console.print()
    
    # Save to file if requested
    if hasattr(args, 'save') and args.save:
        save_result(response, args.save)


def display_comparison_results(results, console, args):
    """Display comparison results in a table format."""
    if not results:
        console.print("[red]No results to display[/red]")
        return
    
    # Create comparison table
    table = Table(title="Model Comparison Results")
    table.add_column("Provider", style="cyan")
    table.add_column("Model Type", style="yellow")
    table.add_column("Model Name", style="green")
    table.add_column("Response Preview", style="white", max_width=50)
    table.add_column("Tokens", style="magenta")
    
    for result in results:
        preview = result.get('response', '')[:100] + "..." if len(result.get('response', '')) > 100 else result.get('response', '')
        token_info = f"{result.get('token_usage', {}).get('total_tokens', 'N/A')}"
        
        table.add_row(
            result.get('provider', 'Unknown'),
            result.get('model_type', 'Unknown'),
            result.get('model_name', 'Unknown'),
            preview,
            token_info
        )
    
    console.print(table)
    console.print()
    
    # Detailed responses
    for i, result in enumerate(results, 1):
        console.print(f"[bold blue]═══ Response {i}: {result.get('provider', 'Unknown')} - {result.get('model_type', 'Unknown')} ═══[/bold blue]")
        console.print(result.get('response', 'No response'))
        console.print()
    
    # Save comparison if requested
    if hasattr(args, 'save') and args.save:
        save_comparison(results, args.save)


def save_result(result, filename):
    """Save single result to file."""
    output_format = filename.split('.')[-1].lower() if '.' in filename else 'json'
    
    if output_format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    elif output_format == 'md':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Model Response\n\n")
            f.write(f"**Model:** {result.get('model_name', 'Unknown')}\n")
            f.write(f"**Provider:** {result.get('provider', 'Unknown')}\n")
            f.write(f"**Type:** {result.get('model_type', 'Unknown')}\n\n")
            f.write(f"## Response\n\n{result.get('response', 'No response')}\n")
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(result))


def save_comparison(results, filename):
    """Save comparison results to file."""
    output_format = filename.split('.')[-1].lower() if '.' in filename else 'json'
    
    if output_format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    elif output_format == 'md':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Model Comparison Results\n\n")
            for i, result in enumerate(results, 1):
                f.write(f"## Response {i}: {result.get('provider', 'Unknown')} - {result.get('model_type', 'Unknown')}\n\n")
                f.write(f"**Model:** {result.get('model_name', 'Unknown')}\n")
                f.write(f"**Response:** {result.get('response', 'No response')}\n\n")


if __name__ == "__main__":
    asyncio.run(main())
