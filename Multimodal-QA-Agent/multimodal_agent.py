import os
import base64
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai

class MultimodalQAAgent:
    """
    A multimodal QA agent using Google Gemini Pro Vision for image analysis
    and question answering, with fallback to text-only responses.
    """
    
    def __init__(self):
        """Initialize the multimodal QA agent."""
        # Get API key from environment
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure the Google Generative AI
        genai.configure(api_key=self.api_key)
        
        # Initialize vision model (Gemini Pro Vision)
        self.vision_model = ChatGoogleGenerativeAI(
            model="gemini-pro-vision",
            google_api_key=self.api_key,
            temperature=0.3
        )
        
        # Initialize text-only model (Gemini Pro) for fallback
        self.text_model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=self.api_key,
            temperature=0.3
        )
        
        # Create prompt templates
        self.vision_prompt = ChatPromptTemplate.from_messages([
            ("human", [
                {
                    "type": "text",
                    "text": "You are an expert image analyst. Analyze the provided image and answer the following question comprehensively and accurately: {question}\n\nProvide detailed observations and insights based on what you can see in the image."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data}"}
                }
            ])
        ])
        
        self.text_prompt = ChatPromptTemplate.from_messages([
            ("human", "I'm asking about an image, but since you can't see it, please provide a general response about what someone might look for when answering this question about an image: {question}\n\nAlso suggest what specific visual elements would be important to observe.")
        ])
    
    def ask_question(self, question: str, image_base64: str) -> str:
        """
        Ask a question about an image using the vision model.
        
        Args:
            question: The question to ask about the image
            image_base64: Base64 encoded image data
            
        Returns:
            The model's response as a string
        """
        try:
            # Format the prompt with the question and image
            formatted_prompt = self.vision_prompt.format_messages(
                question=question,
                image_data=image_base64
            )
            
            # Get response from the vision model
            response = self.vision_model.invoke(formatted_prompt)
            return response.content
            
        except Exception as e:
            raise Exception(f"Vision model failed: {str(e)}")
    
    def ask_question_text_only(self, question: str) -> str:
        """
        Ask a question using only the text model (fallback).
        
        Args:
            question: The question to ask
            
        Returns:
            The model's response as a string
        """
        try:
            # Format the prompt with the question
            formatted_prompt = self.text_prompt.format_messages(question=question)
            
            # Get response from the text model
            response = self.text_model.invoke(formatted_prompt)
            return response.content
            
        except Exception as e:
            raise Exception(f"Text model failed: {str(e)}")
    
    def analyze_image_comprehensive(self, image_base64: str) -> dict:
        """
        Perform comprehensive image analysis.
        
        Args:
            image_base64: Base64 encoded image data
            
        Returns:
            Dictionary containing various analysis results
        """
        analysis_questions = [
            "What are the main objects and subjects in this image?",
            "Describe the colors, lighting, and overall composition",
            "What is the setting or environment shown?",
            "Are there any people in the image? If so, what are they doing?",
            "Is there any text visible in the image?",
            "What is the mood or atmosphere of this image?"
        ]
        
        results = {}
        
        for i, question in enumerate(analysis_questions):
            try:
                answer = self.ask_question(question, image_base64)
                results[f"analysis_{i+1}"] = {
                    "question": question,
                    "answer": answer
                }
            except Exception as e:
                results[f"analysis_{i+1}"] = {
                    "question": question,
                    "answer": f"Analysis failed: {str(e)}"
                }
        
        return results
    
    def get_model_info(self) -> dict:
        """
        Get information about the models being used.
        
        Returns:
            Dictionary with model information
        """
        return {
            "vision_model": "gemini-pro-vision",
            "text_model": "gemini-pro",
            "provider": "Google Generative AI",
            "framework": "LangChain",
            "capabilities": [
                "Image analysis",
                "Text generation",
                "Question answering",
                "Multimodal understanding"
            ]
        }

