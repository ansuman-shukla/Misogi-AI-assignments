"""
Visualization utilities for model comparison results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


class ModelVisualizer:
    """Visualizer for model comparison results."""
    
    def __init__(self, theme: str = 'dark'):
        """
        Initialize visualizer.
        
        Args:
            theme: Color theme ('dark', 'light', 'seaborn')
        """
        self.theme = theme
        self.setup_style()
    
    def setup_style(self):
        """Setup matplotlib and seaborn styling."""
        if self.theme == 'dark':
            plt.style.use('dark_background')
            sns.set_palette("husl")
        elif self.theme == 'seaborn':
            sns.set_style("whitegrid")
            sns.set_palette("deep")
        else:
            plt.style.use('default')
            sns.set_palette("Set2")
    
    def visualize_single_response(self, response: Dict[str, Any]):
        """
        Visualize single model response metrics.
        
        Args:
            response: Model response dictionary
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f"Model Analysis: {response.get('model_name', 'Unknown')}", fontsize=16)
            
            # Token usage breakdown
            token_usage = response.get('token_usage', {})
            if token_usage:
                tokens = ['Input', 'Output']
                values = [token_usage.get('input_tokens', 0), token_usage.get('output_tokens', 0)]
                
                ax1.pie(values, labels=tokens, autopct='%1.1f%%', startangle=90)
                ax1.set_title('Token Usage Distribution')
            
            # Response time vs context window
            context_window = response.get('context_window', 0)
            response_time = response.get('response_time', 0)
            
            ax2.bar(['Context Window', 'Response Time'], 
                   [context_window/1000, response_time*100], 
                   color=['skyblue', 'lightcoral'])
            ax2.set_title('Model Performance Metrics')
            ax2.set_ylabel('Scaled Values')
            
            # Model characteristics radar
            characteristics = response.get('characteristics', {})
            if characteristics:
                self._plot_characteristics_radar(ax3, characteristics)
            
            # Token efficiency
            if token_usage.get('total_tokens', 0) > 0 and response_time > 0:
                efficiency = token_usage['total_tokens'] / response_time
                ax4.bar(['Tokens/Second'], [efficiency], color='green')
                ax4.set_title('Token Generation Efficiency')
                ax4.set_ylabel('Tokens per Second')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Visualization error: {e}")
    
    def visualize_comparison(self, results: List[Dict[str, Any]]):
        """
        Visualize comparison across multiple models.
        
        Args:
            results: List of model response dictionaries
        """
        if not results:
            print("No results to visualize")
            return
        
        try:
            # Create interactive plotly dashboard
            self._create_comparison_dashboard(results)
            
            # Also create matplotlib plots
            self._create_comparison_plots(results)
            
        except Exception as e:
            print(f"Visualization error: {e}")
    
    def _create_comparison_dashboard(self, results: List[Dict[str, Any]]):
        """Create interactive Plotly dashboard."""
        # Prepare data
        df = self._prepare_comparison_dataframe(results)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Token Usage Comparison', 'Response Time Analysis', 
                          'Context Window vs Performance', 'Provider Distribution'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "pie"}]]
        )
        
        # Token usage comparison
        fig.add_trace(
            go.Bar(
                x=df['model_name'],
                y=df['total_tokens'],
                name='Total Tokens',
                marker_color=df['provider'],
                text=df['provider'],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # Response time analysis
        fig.add_trace(
            go.Scatter(
                x=df['model_name'],
                y=df['response_time'],
                mode='markers+lines',
                name='Response Time',
                marker=dict(size=df['total_tokens']/50, color=df['provider']),
                text=df['provider']
            ),
            row=1, col=2
        )
        
        # Context window vs performance
        fig.add_trace(
            go.Scatter(
                x=df['context_window'],
                y=df['total_tokens'],
                mode='markers',
                name='Context vs Tokens',
                marker=dict(
                    size=df['response_time']*10,
                    color=df['provider'],
                    showscale=True
                ),
                text=df['model_name']
            ),
            row=2, col=1
        )
        
        # Provider distribution
        provider_counts = df['provider'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=provider_counts.index,
                values=provider_counts.values,
                name="Provider Distribution"
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title="Model Comparison Dashboard",
            height=800,
            showlegend=True,
            template="plotly_dark" if self.theme == 'dark' else "plotly_white"
        )
        
        fig.show()
    
    def _create_comparison_plots(self, results: List[Dict[str, Any]]):
        """Create matplotlib comparison plots."""
        df = self._prepare_comparison_dataframe(results)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Model Comparison Analysis', fontsize=16)
        
        # 1. Token usage by provider
        provider_tokens = df.groupby('provider')['total_tokens'].mean()
        axes[0, 0].bar(provider_tokens.index, provider_tokens.values)
        axes[0, 0].set_title('Average Token Usage by Provider')
        axes[0, 0].set_ylabel('Total Tokens')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Response time comparison
        axes[0, 1].scatter(df['total_tokens'], df['response_time'], 
                          c=pd.Categorical(df['provider']).codes, alpha=0.7)
        axes[0, 1].set_title('Response Time vs Token Usage')
        axes[0, 1].set_xlabel('Total Tokens')
        axes[0, 1].set_ylabel('Response Time (s)')
        
        # 3. Context window comparison
        axes[0, 2].barh(df['model_name'], df['context_window'])
        axes[0, 2].set_title('Context Window Sizes')
        axes[0, 2].set_xlabel('Context Window Size')
        
        # 4. Model type distribution
        type_counts = df['model_type'].value_counts()
        axes[1, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
        axes[1, 0].set_title('Model Type Distribution')
        
        # 5. Efficiency comparison (tokens per second)
        df['efficiency'] = df['total_tokens'] / df['response_time']
        df_sorted = df.sort_values('efficiency')
        axes[1, 1].barh(df_sorted['model_name'], df_sorted['efficiency'])
        axes[1, 1].set_title('Token Generation Efficiency')
        axes[1, 1].set_xlabel('Tokens per Second')
        
        # 6. Response length distribution
        axes[1, 2].hist([len(r.get('response', '')) for r in results], 
                       bins=10, alpha=0.7, edgecolor='black')
        axes[1, 2].set_title('Response Length Distribution')
        axes[1, 2].set_xlabel('Response Length (characters)')
        axes[1, 2].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.show()
    
    def _prepare_comparison_dataframe(self, results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare DataFrame from results for visualization."""
        data = []
        
        for result in results:
            token_usage = result.get('token_usage', {})
            data.append({
                'provider': result.get('provider', 'Unknown'),
                'model_name': result.get('model_name', 'Unknown'),
                'model_type': result.get('model_type', 'Unknown'),
                'total_tokens': token_usage.get('total_tokens', 0),
                'input_tokens': token_usage.get('input_tokens', 0),
                'output_tokens': token_usage.get('output_tokens', 0),
                'response_time': result.get('response_time', 0),
                'context_window': result.get('context_window', 0),
                'response_length': len(result.get('response', '')),
                'has_error': bool(result.get('error'))
            })
        
        return pd.DataFrame(data)
    
    def _plot_characteristics_radar(self, ax, characteristics: Dict[str, Any]):
        """Plot model characteristics as radar chart."""
        try:
            # Extract numeric characteristics
            numeric_chars = {}
            
            # Map characteristics to numeric values
            if 'context_window' in characteristics:
                numeric_chars['Context Window'] = min(characteristics['context_window'] / 10000, 10)
            
            instruction_mapping = {
                'basic': 3, 'good': 5, 'very good': 7, 
                'excellent': 9, 'outstanding': 10
            }
            
            if 'instruction_following' in characteristics:
                inst_val = characteristics['instruction_following'].lower()
                numeric_chars['Instruction Following'] = instruction_mapping.get(inst_val, 5)
            
            # Create simple bar chart instead of radar for simplicity
            if numeric_chars:
                keys = list(numeric_chars.keys())
                values = list(numeric_chars.values())
                ax.bar(keys, values)
                ax.set_title('Model Characteristics')
                ax.tick_params(axis='x', rotation=45)
            else:
                ax.text(0.5, 0.5, 'No numeric\ncharacteristics\navailable', 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title('Model Characteristics')
                
        except Exception as e:
            ax.text(0.5, 0.5, f'Error plotting\ncharacteristics:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def save_comparison_report(self, results: List[Dict[str, Any]], filename: str = 'comparison_report.html'):
        """
        Generate and save an HTML comparison report.
        
        Args:
            results: List of model response dictionaries
            filename: Output filename
        """
        try:
            df = self._prepare_comparison_dataframe(results)
            
            # Create comprehensive report
            html_content = self._generate_html_report(df, results)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Comparison report saved to {filename}")
            
        except Exception as e:
            print(f"Error generating report: {e}")
    
    def _generate_html_report(self, df: pd.DataFrame, results: List[Dict[str, Any]]) -> str:
        """Generate HTML report content."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Model Comparison Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .model-result {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .stats {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Model Comparison Report</h1>
                <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>Summary Statistics</h2>
                <div class="stats">
                    <p><strong>Total Models Tested:</strong> {len(results)}</p>
                    <p><strong>Providers:</strong> {', '.join(df['provider'].unique())}</p>
                    <p><strong>Model Types:</strong> {', '.join(df['model_type'].unique())}</p>
                    <p><strong>Average Response Time:</strong> {df['response_time'].mean():.2f} seconds</p>
                    <p><strong>Average Token Usage:</strong> {df['total_tokens'].mean():.0f} tokens</p>
                </div>
            </div>
            
            <div class="detailed-results">
                <h2>Detailed Results</h2>
                {self._generate_detailed_results_html(results)}
            </div>
            
            <div class="comparison-table">
                <h2>Comparison Table</h2>
                {df.to_html(table_id='comparison-table', classes='table table-striped')}
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_detailed_results_html(self, results: List[Dict[str, Any]]) -> str:
        """Generate detailed results HTML."""
        html_parts = []
        
        for i, result in enumerate(results, 1):
            provider = result.get('provider', 'Unknown')
            model_name = result.get('model_name', 'Unknown')
            model_type = result.get('model_type', 'Unknown')
            response = result.get('response', 'No response')
            token_usage = result.get('token_usage', {})
            
            html_parts.append(f"""
            <div class="model-result">
                <h3>Result {i}: {provider} - {model_name}</h3>
                <p><strong>Model Type:</strong> {model_type}</p>
                <p><strong>Response Time:</strong> {result.get('response_time', 0):.2f} seconds</p>
                <p><strong>Token Usage:</strong> {token_usage.get('total_tokens', 'N/A')} 
                   (Input: {token_usage.get('input_tokens', 'N/A')}, Output: {token_usage.get('output_tokens', 'N/A')})</p>
                <div class="response">
                    <h4>Response:</h4>
                    <p>{response[:500]}{'...' if len(response) > 500 else ''}</p>
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
