"""
Interactive mode for the model comparison tool.
"""

import asyncio
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint


class InteractiveMode:
    """Interactive command-line interface for model comparison."""
    
    def __init__(self, console: Console, config: Dict[str, Any]):
        self.console = console
        self.config = config
        self.session_history: List[Dict[str, Any]] = []
    
    async def run(self):
        """Run the interactive mode."""
        self.show_welcome()
        
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == '1':
                    await self.single_query_mode()
                elif choice == '2':
                    await self.comparison_mode()
                elif choice == '3':
                    self.show_model_info()
                elif choice == '4':
                    self.show_session_history()
                elif choice == '5':
                    self.show_settings()
                elif choice == '6':
                    self.show_help()
                elif choice == '7':
                    if Confirm.ask("Are you sure you want to exit?"):
                        self.console.print("[green]Goodbye![/green]")
                        break
                else:
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
                    
            except KeyboardInterrupt:
                if Confirm.ask("\nDo you want to exit?"):
                    break
                else:
                    continue
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def show_welcome(self):
        """Display welcome message and tool overview."""
        welcome_text = """
[bold blue]🤖 Model Comparison and Use-case Mapping Tool[/bold blue]

Compare responses from different AI models:
• [cyan]OpenAI[/cyan] (GPT-3.5, GPT-4)
• [cyan]Anthropic[/cyan] (Claude models)  
• [cyan]Hugging Face[/cyan] (Open source models)

Model Types:
• [yellow]Base[/yellow]: Foundation models for completion
• [yellow]Instruct[/yellow]: Instruction-following models
• [yellow]Fine-tuned[/yellow]: Domain-specialized models
        """
        
        panel = Panel(welcome_text, title="Welcome", border_style="blue")
        self.console.print(panel)
        self.console.print()
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        menu_options = [
            "1. Single Model Query",
            "2. Compare Multiple Models", 
            "3. View Model Information",
            "4. View Session History",
            "5. Settings",
            "6. Help",
            "7. Exit"
        ]
        
        self.console.print("[bold cyan]Main Menu:[/bold cyan]")
        for option in menu_options:
            self.console.print(f"  {option}")
        self.console.print()
        
        return Prompt.ask("Choose an option", choices=['1', '2', '3', '4', '5', '6', '7'])
    
    async def single_query_mode(self):
        """Handle single model query in interactive mode."""
        self.console.print("[bold green]Single Model Query[/bold green]")
        self.console.print()
        
        # Get query from user
        query = Prompt.ask("Enter your query")
        if not query.strip():
            self.console.print("[red]Query cannot be empty[/red]")
            return
        
        # Select provider
        provider = Prompt.ask(
            "Choose provider",
            choices=['openai', 'anthropic', 'huggingface'],
            default='openai'
        )
        
        # Select model type
        model_type = Prompt.ask(
            "Choose model type",
            choices=['base', 'instruct', 'fine-tuned'],
            default='instruct'
        )
        
        # Optional specific model
        use_specific = Confirm.ask("Use specific model name?", default=False)
        model_name = None
        if use_specific:
            model_name = Prompt.ask("Enter model name")
        
        # Generate response
        try:
            from providers.provider_factory import ProviderFactory
            
            provider_factory = ProviderFactory(self.config)
            provider_instance = provider_factory.get_provider(provider)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"Querying {provider} model...", total=None)
                
                response = await provider_instance.generate_response(
                    query=query,
                    model_type=model_type,
                    model_name=model_name
                )
                
                progress.stop()
            
            # Display result
            self.display_single_response(response)
            
            # Add to session history
            self.session_history.append({
                'type': 'single_query',
                'query': query,
                'provider': provider,
                'model_type': model_type,
                'model_name': model_name,
                'response': response
            })
            
            # Ask if user wants to save
            if Confirm.ask("Save this result?", default=False):
                filename = Prompt.ask("Enter filename", default="result.json")
                self.save_response(response, filename)
                
        except Exception as e:
            self.console.print(f"[red]Error generating response: {str(e)}[/red]")
    
    async def comparison_mode(self):
        """Handle multi-model comparison in interactive mode."""
        self.console.print("[bold green]Multi-Model Comparison[/bold green]")
        self.console.print()
        
        # Get query
        query = Prompt.ask("Enter your query")
        if not query.strip():
            self.console.print("[red]Query cannot be empty[/red]")
            return
        
        # Select providers to compare
        self.console.print("Select providers to compare:")
        providers = []
        
        for provider in ['openai', 'anthropic', 'huggingface']:
            if Confirm.ask(f"Include {provider}?", default=True):
                providers.append(provider)
        
        if not providers:
            self.console.print("[red]At least one provider must be selected[/red]")
            return
        
        # Select model types
        self.console.print("Select model types to compare:")
        model_types = []
        
        for model_type in ['base', 'instruct', 'fine-tuned']:
            if Confirm.ask(f"Include {model_type} models?", default=True):
                model_types.append(model_type)
        
        if not model_types:
            self.console.print("[red]At least one model type must be selected[/red]")
            return
        
        # Generate comparisons
        try:
            from providers.provider_factory import ProviderFactory
            
            provider_factory = ProviderFactory(self.config)
            results = []
            
            total_combinations = len(providers) * len(model_types)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                
                for provider_name in providers:
                    provider_instance = provider_factory.get_provider(provider_name)
                    
                    for model_type in model_types:
                        task = progress.add_task(
                            f"Querying {provider_name} {model_type}...", 
                            total=None
                        )
                        
                        try:
                            response = await provider_instance.generate_response(
                                query=query,
                                model_type=model_type
                            )
                            results.append(response)
                            
                        except Exception as e:
                            self.console.print(f"[yellow]Warning: Failed {provider_name} {model_type}: {str(e)}[/yellow]")
                        
                        progress.remove_task(task)
            
            # Display comparison results
            self.display_comparison_results(results)
            
            # Add to session history
            self.session_history.append({
                'type': 'comparison',
                'query': query,
                'providers': providers,
                'model_types': model_types,
                'results': results
            })
            
            # Ask for visualization
            if Confirm.ask("Show visualization?", default=False):
                try:
                    from utils.visualization import ModelVisualizer
                    visualizer = ModelVisualizer()
                    visualizer.visualize_comparison(results)
                except Exception as e:
                    self.console.print(f"[red]Visualization error: {str(e)}[/red]")
            
            # Ask if user wants to save
            if Confirm.ask("Save comparison results?", default=False):
                filename = Prompt.ask("Enter filename", default="comparison.json")
                self.save_comparison(results, filename)
                
        except Exception as e:
            self.console.print(f"[red]Error in comparison mode: {str(e)}[/red]")
    
    def show_model_info(self):
        """Display information about available models."""
        self.console.print("[bold cyan]Available Models Information[/bold cyan]")
        self.console.print()
        
        # Create model info table
        table = Table(title="Model Information")
        table.add_column("Provider", style="cyan")
        table.add_column("Model Type", style="yellow")
        table.add_column("Model Name", style="green")
        table.add_column("Context Window", style="blue")
        table.add_column("Characteristics", style="white")
        
        # Model information data
        models_info = [
            ("OpenAI", "Instruct", "gpt-3.5-turbo", "4,096", "Fast, cost-effective"),
            ("OpenAI", "Instruct", "gpt-4", "8,192", "Advanced reasoning"),
            ("OpenAI", "Instruct", "gpt-4-turbo", "128,000", "Large context, multimodal"),
            ("Anthropic", "Instruct", "claude-3-haiku", "200,000", "Fast, efficient"),
            ("Anthropic", "Instruct", "claude-3-sonnet", "200,000", "Balanced performance"),
            ("Anthropic", "Instruct", "claude-3-opus", "200,000", "Highest capability"),
            ("HuggingFace", "Base", "meta-llama/Llama-2-7b", "4,096", "Open source base"),
            ("HuggingFace", "Instruct", "meta-llama/Llama-2-7b-chat", "4,096", "Chat optimized"),
            ("HuggingFace", "Fine-tuned", "codellama/CodeLlama-7b", "4,096", "Code generation"),
        ]
        
        for provider, model_type, name, context, characteristics in models_info:
            table.add_row(provider, model_type, name, context, characteristics)
        
        self.console.print(table)
        self.console.print()
        
        # Model type explanations
        explanations = Panel("""
[bold yellow]Model Types Explained:[/bold yellow]

[cyan]Base Models:[/cyan] Foundation models trained on large text corpora
• Best for: Text completion, creative writing
• Characteristics: Require careful prompting

[cyan]Instruct Models:[/cyan] Fine-tuned to follow instructions  
• Best for: Q&A, task completion, general assistance
• Characteristics: Better instruction following

[cyan]Fine-tuned Models:[/cyan] Specialized for specific domains
• Best for: Code generation, domain-specific tasks
• Characteristics: Optimized for particular use cases
        """, title="Model Type Guide", border_style="yellow")
        
        self.console.print(explanations)
    
    def show_session_history(self):
        """Display session history."""
        if not self.session_history:
            self.console.print("[yellow]No queries in session history[/yellow]")
            return
        
        self.console.print(f"[bold cyan]Session History ({len(self.session_history)} entries)[/bold cyan]")
        self.console.print()
        
        for i, entry in enumerate(self.session_history, 1):
            query_preview = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
            
            if entry['type'] == 'single_query':
                self.console.print(f"{i}. [green]Single Query[/green]: {query_preview}")
                self.console.print(f"   Provider: {entry['provider']}, Type: {entry['model_type']}")
            else:
                self.console.print(f"{i}. [blue]Comparison[/blue]: {query_preview}")
                self.console.print(f"   Providers: {', '.join(entry['providers'])}")
            self.console.print()
        
        # Option to view details
        if Confirm.ask("View details for a specific entry?", default=False):
            try:
                entry_num = int(Prompt.ask("Enter entry number")) - 1
                if 0 <= entry_num < len(self.session_history):
                    self.show_history_entry_details(self.session_history[entry_num])
                else:
                    self.console.print("[red]Invalid entry number[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
    
    def show_history_entry_details(self, entry: Dict[str, Any]):
        """Show details for a specific history entry."""
        self.console.print(f"[bold green]Query:[/bold green] {entry['query']}")
        self.console.print()
        
        if entry['type'] == 'single_query':
            self.display_single_response(entry['response'])
        else:
            self.display_comparison_results(entry['results'])
    
    def show_settings(self):
        """Display and modify settings."""
        self.console.print("[bold cyan]Settings[/bold cyan]")
        self.console.print()
        
        settings_info = f"""
Current Settings:
• Max Tokens: {self.config.get('max_tokens', 1000)}
• Temperature: {self.config.get('temperature', 0.7)}
• Timeout: {self.config.get('timeout', 30)}s
• Log Level: {self.config.get('log_level', 'INFO')}
        """
        
        self.console.print(settings_info)
        
        if Confirm.ask("Modify settings?", default=False):
            # Allow user to modify settings
            new_max_tokens = Prompt.ask(
                "Max tokens", 
                default=str(self.config.get('max_tokens', 1000))
            )
            new_temperature = Prompt.ask(
                "Temperature (0.0-2.0)", 
                default=str(self.config.get('temperature', 0.7))
            )
            
            try:
                self.config['max_tokens'] = int(new_max_tokens)
                self.config['temperature'] = float(new_temperature)
                self.console.print("[green]Settings updated![/green]")
            except ValueError:
                self.console.print("[red]Invalid values entered[/red]")
    
    def show_help(self):
        """Display help information."""
        help_text = """
[bold cyan]Help - Model Comparison Tool[/bold cyan]

[yellow]Navigation:[/yellow]
• Use number keys to select menu options
• Ctrl+C to interrupt current operation
• Type responses when prompted

[yellow]Query Tips:[/yellow]
• Be specific in your questions
• Try different phrasings to compare responses
• Use technical terms for code-related queries

[yellow]Model Selection:[/yellow]
• Base: For completion tasks
• Instruct: For question answering
• Fine-tuned: For specialized domains

[yellow]Comparison Mode:[/yellow]
• Select multiple providers/types
• Compare responses side-by-side
• Analyze differences in approach

[yellow]Visualization:[/yellow]
• View token usage patterns
• Compare response times
• Analyze model characteristics
        """
        
        panel = Panel(help_text, title="Help", border_style="cyan")
        self.console.print(panel)
    
    def display_single_response(self, response: Dict[str, Any]):
        """Display a single model response."""
        # Create response panel
        response_text = response.get('response', 'No response')
        model_info = f"Model: {response.get('model_name', 'Unknown')} | Provider: {response.get('provider', 'Unknown')}"
        
        panel = Panel(response_text, title=model_info, border_style="green")
        self.console.print(panel)
        
        # Show characteristics if available
        if 'characteristics' in response:
            char_text = ""
            for key, value in response['characteristics'].items():
                char_text += f"• {key}: {value}\n"
            
            char_panel = Panel(char_text, title="Model Characteristics", border_style="yellow")
            self.console.print(char_panel)
        
        # Show token usage if available
        if 'token_usage' in response:
            usage = response['token_usage']
            usage_text = f"""
Input tokens: {usage.get('input_tokens', 'N/A')}
Output tokens: {usage.get('output_tokens', 'N/A')}
Total tokens: {usage.get('total_tokens', 'N/A')}
            """
            usage_panel = Panel(usage_text.strip(), title="Token Usage", border_style="magenta")
            self.console.print(usage_panel)
    
    def display_comparison_results(self, results: List[Dict[str, Any]]):
        """Display comparison results."""
        if not results:
            self.console.print("[red]No results to display[/red]")
            return
        
        # Summary table
        table = Table(title="Comparison Summary")
        table.add_column("Provider", style="cyan")
        table.add_column("Model Type", style="yellow")
        table.add_column("Model", style="green")
        table.add_column("Response Length", style="blue")
        table.add_column("Tokens", style="magenta")
        
        for result in results:
            response_len = len(result.get('response', ''))
            tokens = result.get('token_usage', {}).get('total_tokens', 'N/A')
            
            table.add_row(
                result.get('provider', 'Unknown'),
                result.get('model_type', 'Unknown'),
                result.get('model_name', 'Unknown')[:20],
                str(response_len),
                str(tokens)
            )
        
        self.console.print(table)
        self.console.print()
        
        # Detailed responses
        for i, result in enumerate(results, 1):
            model_info = f"{result.get('provider', 'Unknown')} - {result.get('model_type', 'Unknown')}"
            response_text = result.get('response', 'No response')
            
            panel = Panel(response_text, title=f"Response {i}: {model_info}", border_style="blue")
            self.console.print(panel)
    
    def save_response(self, response: Dict[str, Any], filename: str):
        """Save single response to file."""
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
            self.console.print(f"[green]Response saved to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error saving file: {str(e)}[/red]")
    
    def save_comparison(self, results: List[Dict[str, Any]], filename: str):
        """Save comparison results to file."""
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.console.print(f"[green]Comparison saved to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error saving file: {str(e)}[/red]")
