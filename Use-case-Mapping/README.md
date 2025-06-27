# Model Comparison and Use-case Mapping Tool

A comprehensive command-line tool for comparing Base, Instruct, and Fine-tuned models from popular AI providers (OpenAI, Anthropic, and Hugging Face).

## 🚀 Features

- **Multi-provider Support**: Compare models from OpenAI, Anthropic, and Hugging Face
- **Model Type Comparison**: Base vs Instruct vs Fine-tuned models
- **Interactive CLI**: Easy-to-use command-line interface with rich formatting
- **Token Usage Visualization**: Visual representation of token consumption
- **Context Window Analysis**: Compare context window lengths across models
- **Comprehensive Logging**: Detailed comparison logs and results
- **Flexible Configuration**: Support for multiple API keys and custom settings

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Use-case-Mapping
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## ⚙️ Configuration

Create a `.env` file based on `.env.example` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

## 📋 Usage

### Basic Usage

```bash
python main.py --query "Explain quantum computing" --provider openai --model-type instruct
```

### Advanced Usage

```bash
# Compare multiple models
python main.py --query "Write a Python function to sort a list" --compare-all

# Specific model comparison
python main.py --query "Explain machine learning" --provider anthropic --model claude-3-sonnet --visualize

# Interactive mode
python main.py --interactive
```

### Command Line Arguments

- `--query, -q`: Input query for the models
- `--provider, -p`: Choose provider (openai, anthropic, huggingface)
- `--model-type, -t`: Model type (base, instruct, fine-tuned)
- `--model, -m`: Specific model name
- `--compare-all, -c`: Compare across all available models
- `--visualize, -v`: Show token usage and context window visualization
- `--interactive, -i`: Start interactive mode
- `--output, -o`: Output format (console, json, markdown)
- `--save`: Save results to file

## 🧠 Model Types Explained

### Base Models
- **Purpose**: Foundation models trained on large text corpora
- **Characteristics**: Good at completion tasks, require careful prompting
- **Use Cases**: Text completion, creative writing, research applications
- **Examples**: GPT-3 Base, Claude Base models

### Instruct Models
- **Purpose**: Models fine-tuned to follow instructions
- **Characteristics**: Better at understanding and following commands
- **Use Cases**: Question answering, task completion, general assistance
- **Examples**: GPT-3.5/4 Instruct, Claude-3, Llama-2-Chat

### Fine-tuned Models
- **Purpose**: Models specialized for specific domains or tasks
- **Characteristics**: Optimized performance for particular use cases
- **Use Cases**: Code generation, medical queries, legal analysis
- **Examples**: CodeLlama, GPT-4 Fine-tuned variants

## 📊 Example Comparisons

See `comparisons.md` for detailed analysis of model performance across different query types.

## 🏗️ Project Structure

```
Use-case-Mapping/
├── src/
│   ├── providers/
│   │   ├── openai_provider.py
│   │   ├── anthropic_provider.py
│   │   └── huggingface_provider.py
│   ├── models/
│   │   ├── base_model.py
│   │   └── model_config.py
│   ├── utils/
│   │   ├── visualization.py
│   │   ├── tokenizer.py
│   │   └── logger.py
│   └── cli/
│       ├── parser.py
│       └── interactive.py
├── config/
│   └── models.yaml
├── tests/
├── main.py
├── requirements.txt
├── .env.example
├── comparisons.md
└── README.md
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📈 Visualization Features

The tool provides visual representations of:
- Token usage across different models
- Context window utilization
- Response time comparisons
- Model performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com)
- [Hugging Face API Documentation](https://huggingface.co/docs/api-inference)
