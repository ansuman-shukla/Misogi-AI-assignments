import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO
import base64
from multimodal_agent import MultimodalQAAgent

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Multimodal QA Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Multimodal QA Agent")
    st.markdown("Ask questions about images using Google Gemini Pro Vision!")
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = MultimodalQAAgent()
        except Exception as e:
            st.error(f"Failed to initialize the agent: {str(e)}")
            st.info("Please make sure you have set your GOOGLE_API_KEY in the .env file")
            return
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        model_type = st.selectbox(
            "Select Model",
            ["Gemini Pro Vision (Multimodal)", "Gemini Pro (Text-only)"],
            index=0
        )
        
        st.header("About")
        st.info(
            "This app uses Google's Gemini Pro Vision model to analyze images and answer questions. "
            "Upload an image or provide a URL, then ask any question about it!"
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Image Input")
        
        # Image input options
        input_method = st.radio(
            "Choose input method:",
            ["Upload Image", "Image URL"]
        )
        
        image = None
        image_data = None
        
        if input_method == "Upload Image":
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp']
            )
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                image_data = uploaded_file.getvalue()
        
        else:  # Image URL
            image_url = st.text_input("Enter image URL:")
            if image_url:
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    image = Image.open(BytesIO(response.content))
                    image_data = response.content
                except Exception as e:
                    st.error(f"Failed to load image from URL: {str(e)}")
        
        # Display image if available
        if image:
            st.image(image, caption="Input Image", use_column_width=True)
    
    with col2:
        st.header("❓ Question & Answer")
        
        # Question input
        question = st.text_area(
            "Ask a question about the image:",
            placeholder="What do you see in this image?",
            height=100
        )
        
        # Generate answer button
        if st.button("🚀 Get Answer", type="primary"):
            if image is None:
                st.warning("Please upload an image or provide an image URL first.")
            elif not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Analyzing image and generating answer..."):
                    try:
                        # Determine if we should use multimodal or text-only
                        use_vision = model_type == "Gemini Pro Vision (Multimodal)"
                        
                        if use_vision and image_data:
                            # Convert image to base64 for the API
                            image_b64 = base64.b64encode(image_data).decode()
                            answer = st.session_state.agent.ask_question(question, image_b64)
                        else:
                            # Text-only fallback
                            answer = st.session_state.agent.ask_question_text_only(question)
                        
                        st.success("Answer generated successfully!")
                        st.markdown("### 🤖 AI Response:")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
                        # Try fallback
                        if use_vision:
                            st.info("Trying text-only fallback...")
                            try:
                                answer = st.session_state.agent.ask_question_text_only(question)
                                st.markdown("### 🤖 AI Response (Text-only fallback):")
                                st.markdown(answer)
                            except Exception as fallback_e:
                                st.error(f"Fallback also failed: {str(fallback_e)}")
    
    # Example section
    st.header("💡 Example Questions")
    st.markdown("""
    Try asking questions like:
    - "What objects do you see in this image?"
    - "Describe the colors and composition"
    - "What is the mood or atmosphere of this scene?"
    - "Can you identify any text in the image?"
    - "What activities are happening in this image?"
    - "Describe the setting and environment"
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit, LangChain, and Google Gemini Pro Vision")

if __name__ == "__main__":
    main()
