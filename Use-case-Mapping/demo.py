#!/usr/bin/env python3
"""
Demo script for the Model Comparison Tool.
This script demonstrates the basic functionality with sample queries.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.model_config import load_config
from providers.provider_factory import ProviderFactory
from utils.logger import setup_logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


async def demo_single_query():
    """Demonstrate single model query."""
    console = Console()
    console.print("[bold blue]Demo 1: Single Model Query[/bold blue]")
    
    try:
        config = load_config()
        logger = setup_logger()
        
        # Check if we have any API keys
        factory = ProviderFactory(config)
        available_providers = factory.get_available_providers()
        
        if not available_providers:
            console.print("[red]No API keys found. Please set up your .env file with API keys.[/red]")
            console.print("See INSTALL.md for instructions on getting API keys.")
            return
        
        provider_name = available_providers[0]
        console.print(f"Using provider: {provider_name}")
        
        provider = factory.get_provider(provider_name)
        
        query = "Explain the difference between machine learning and artificial intelligence in simple terms."
        
        console.print(f"[cyan]Query:[/cyan] {query}")
        console.print()
        
        with console.status("[bold green]Generating response..."):
            response = await provider.generate_response(
                query=query,
                model_type='instruct'
            )
        
        # Display result
        panel = Panel(
            response.get('response', 'No response'),
            title=f"Response from {response.get('model_name', 'Unknown')}",
            border_style="green"
        )
        console.print(panel)
        
        # Show metadata
        metadata_table = Table(title="Response Metadata")
        metadata_table.add_column("Metric", style="cyan")
        metadata_table.add_column("Value", style="yellow")
        
        token_usage = response.get('token_usage', {})
        metadata_table.add_row("Provider", response.get('provider', 'Unknown'))
        metadata_table.add_row("Model", response.get('model_name', 'Unknown'))
        metadata_table.add_row("Response Time", f"{response.get('response_time', 0):.2f}s")
        metadata_table.add_row("Total Tokens", str(token_usage.get('total_tokens', 'N/A')))
        
        console.print(metadata_table)
        
    except Exception as e:
        console.print(f"[red]Error in demo: {str(e)}[/red]")


async def demo_comparison():
    """Demonstrate model comparison."""
    console = Console()
    console.print("\n[bold blue]Demo 2: Model Comparison[/bold blue]")
    
    try:
        config = load_config()
        factory = ProviderFactory(config)
        available_providers = factory.get_available_providers()
        
        if len(available_providers) < 2:
            console.print("[yellow]Need at least 2 providers for comparison demo.[/yellow]")
            console.print("Add more API keys to see comparison functionality.")
            return
        
        query = "Write a Python function to calculate the factorial of a number."
        console.print(f"[cyan]Query:[/cyan] {query}")
        console.print()
        
        results = []
        
        for provider_name in available_providers[:2]:  # Compare first 2 providers
            try:
                provider = factory.get_provider(provider_name)
                
                with console.status(f"[bold green]Querying {provider_name}..."):
                    response = await provider.generate_response(
                        query=query,
                        model_type='instruct'
                    )
                    results.append(response)
                    
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to query {provider_name}: {str(e)}[/yellow]")
        
        # Display comparison
        if results:
            comparison_table = Table(title="Model Comparison Results")
            comparison_table.add_column("Provider", style="cyan")
            comparison_table.add_column("Model", style="green")
            comparison_table.add_column("Response Time", style="yellow")
            comparison_table.add_column("Tokens", style="magenta")
            comparison_table.add_column("Response Preview", style="white", max_width=50)
            
            for result in results:
                preview = result.get('response', '')[:100] + "..." if len(result.get('response', '')) > 100 else result.get('response', '')
                token_info = str(result.get('token_usage', {}).get('total_tokens', 'N/A'))
                response_time = f"{result.get('response_time', 0):.2f}s"
                
                comparison_table.add_row(
                    result.get('provider', 'Unknown'),
                    result.get('model_name', 'Unknown'),
                    response_time,
                    token_info,
                    preview
                )
            
            console.print(comparison_table)
            
            # Show detailed responses
            for i, result in enumerate(results, 1):
                panel = Panel(
                    result.get('response', 'No response'),
                    title=f"Response {i}: {result.get('provider', 'Unknown')} - {result.get('model_name', 'Unknown')}",
                    border_style="blue"
                )
                console.print(panel)
        
    except Exception as e:
        console.print(f"[red]Error in comparison demo: {str(e)}[/red]")


def demo_config():
    """Demonstrate configuration functionality."""
    console = Console()
    console.print("\n[bold blue]Demo 3: Configuration Overview[/bold blue]")
    
    try:
        config = load_config()
        
        config_table = Table(title="Current Configuration")
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="yellow")
        
        # Show non-sensitive config
        config_table.add_row("Max Tokens", str(config.get('max_tokens', 'Not set')))
        config_table.add_row("Temperature", str(config.get('temperature', 'Not set')))
        config_table.add_row("Request Timeout", f"{config.get('timeout', 'Not set')}s")
        config_table.add_row("Log Level", config.get('log_level', 'Not set'))
        
        # Show API key status (without revealing keys)
        api_status = []
        if config.get('openai_api_key'):
            api_status.append("OpenAI ✓")
        if config.get('anthropic_api_key'):
            api_status.append("Anthropic ✓")
        if config.get('huggingface_api_key'):
            api_status.append("HuggingFace ✓")
        
        config_table.add_row("API Keys", ", ".join(api_status) if api_status else "None configured")
        
        console.print(config_table)
        
        # Show available models
        models_config = config.get('models', {})
        if models_config:
            console.print("\n[bold green]Available Model Types:[/bold green]")
            
            for provider, types in models_config.items():
                console.print(f"\n[cyan]{provider.title()}:[/cyan]")
                for model_type, info in types.items():
                    if info.get('models'):
                        console.print(f"  • {model_type}: {len(info['models'])} models")
                    else:
                        console.print(f"  • {model_type}: No models available")
        
    except Exception as e:
        console.print(f"[red]Error showing config: {str(e)}[/red]")


async def main():
    """Run all demos."""
    console = Console()
    
    welcome_text = """
[bold blue]🤖 Model Comparison Tool Demo[/bold blue]

This demo shows the basic functionality of the tool:
1. Single model queries
2. Model comparison
3. Configuration overview

Make sure you have set up your API keys in the .env file!
    """
    
    panel = Panel(welcome_text, title="Welcome", border_style="blue")
    console.print(panel)
    
    # Run demos
    await demo_single_query()
    await demo_comparison()
    demo_config()
    
    console.print("\n[bold green]Demo completed![/bold green]")
    console.print("Try running the tool with: python main.py --interactive")


if __name__ == "__main__":
    asyncio.run(main())
