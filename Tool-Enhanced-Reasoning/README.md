# Tool-Enhanced Reasoning

This project demonstrates tool-enhanced reasoning using Google's Gemini AI with custom function calling capabilities.

## Project Structure

```
├── main.py              # Main application file with Gemini AI integration
├── tools/               # Directory containing tool modules
│   ├── math_tools.py    # Mathematical operations and calculations
│   └── string_tools.py  # String manipulation and processing tools
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Gemini API key as an environment variable:
   ```bash
   set GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the main application:
```bash
python main.py
```

## Features

- **Math Tools**: Perform various mathematical operations including addition, subtraction, multiplication, division, power calculations, and factorial computation
- **String Tools**: Handle string manipulations such as reversing, case conversion, word counting, palindrome checking, and substring replacement
- **AI Integration**: Uses Google's Gemini 2.0 Flash model with function calling capabilities

## Tools Available

### Math Tools (`tools/math_tools.py`)
- `add(a, b)` - Addition
- `subtract(a, b)` - Subtraction
- `multiply(a, b)` - Multiplication
- `divide(a, b)` - Division
- `power(base, exponent)` - Exponentiation
- `factorial(n)` - Factorial calculation

### String Tools (`tools/string_tools.py`)
- `reverse_string(s)` - Reverse a string
- `count_characters(s)` - Count characters
- `count_words(s)` - Count words
- `to_uppercase(s)` - Convert to uppercase
- `to_lowercase(s)` - Convert to lowercase
- `capitalize_words(s)` - Capitalize each word
- `remove_whitespace(s)` - Remove leading/trailing whitespace
- `replace_substring(s, old, new)` - Replace substrings
- `is_palindrome(s)` - Check if string is palindrome
