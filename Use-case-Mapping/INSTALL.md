## Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- API keys for desired providers (OpenAI, Anthropic, Hugging Face)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd Use-case-Mapping
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your API keys:
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key
   HUGGINGFACE_API_KEY=your_actual_huggingface_api_key
   ```

### Step 5: Verify Installation
```bash
python main.py --help
```

## Getting API Keys

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Anthropic API Key
1. Visit [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Hugging Face API Key
1. Visit [Hugging Face](https://huggingface.co)
2. Sign up or log in to your account
3. Go to Settings > Access Tokens
4. Create a new token with read access
5. Copy the token to your `.env` file

## Usage Examples

### Basic Query
```bash
python main.py --query "Explain machine learning" --provider openai
```

### Compare All Models
```bash
python main.py --query "Write a Python function to sort a list" --compare-all
```

### Interactive Mode
```bash
python main.py --interactive
```

### Save Results
```bash
python main.py --query "Explain quantum computing" --save results.json --visualize
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've activated your virtual environment and installed all dependencies
2. **API Key Errors**: Verify your API keys are correctly set in the `.env` file
3. **Permission Errors**: Ensure you have write permissions in the project directory
4. **Module Not Found**: Check that you're running commands from the project root directory

### Getting Help
- Check the console output for detailed error messages
- Use `--debug` flag for more verbose error information
- Review the logs in `model_comparisons.log`
