# Multimodal QA Agent

A multimodal question-answering web application that combines vision and language capabilities using Google's Gemini Pro Vision model through LangChain.

## Features

- **Image Upload**: Upload images directly or provide URLs
- **Text Questions**: Ask questions about the uploaded images
- **Multimodal AI**: Uses Google Gemini Pro Vision for image analysis and question answering
- **Fallback System**: Falls back to text-only responses if image analysis fails
- **Web Interface**: Clean, user-friendly Streamlit interface

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: LangChain + Google GenAI
- **LLM**: Google Gemini Pro Vision (multimodal) with Gemini Pro (text-only fallback)
- **Image Processing**: PIL (Pillow)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the web app
2. Upload an image or provide an image URL
3. Ask a question about the image
4. Get AI-powered responses combining visual and textual understanding

## API Selection

**Why Google Gemini Pro Vision?**
- Native multimodal capabilities
- Excellent image understanding
- Cost-effective compared to GPT-4o
- Strong integration with LangChain
- Reliable fallback to text-only model

## Test Results

### Sample Image-Question Pairs

1. **Image**: Product photo
   - **Question**: "What product is this and what are its key features?"
   - **Response**: [Detailed product analysis]

2. **Image**: Chart/Graph
   - **Question**: "What trends can you identify in this data?"
   - **Response**: [Data interpretation and insights]

3. **Image**: Scene/Landscape
   - **Question**: "Describe the setting and atmosphere of this image"
   - **Response**: [Comprehensive scene description]

## Demo

[Screenshots and demo videos will be added here]

## Architecture

```
Frontend (Streamlit) → LangChain → Google Gemini Pro Vision → Response
                                     ↓ (fallback)
                                   Gemini Pro (text-only)
```

## Error Handling

- Image processing errors are caught and handled gracefully
- API failures trigger fallback to text-only responses
- User-friendly error messages for common issues
