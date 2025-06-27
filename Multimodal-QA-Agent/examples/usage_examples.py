"""
Example usage of the Multimodal QA Agent.
This script shows how to use the agent programmatically.
"""

import os
from dotenv import load_dotenv
from multimodal_agent import MultimodalQAAgent
from utils import prepare_image_for_api, log_interaction
import json

def example_basic_usage():
    """Basic example of using the multimodal agent."""
    print("🚀 Basic Usage Example")
    print("-" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize agent
    try:
        agent = MultimodalQAAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Example questions for text-only mode
    text_questions = [
        "What should I look for when analyzing a product image?",
        "How can I describe the composition of a photograph?",
        "What elements make a good data visualization?"
    ]
    
    print("\n📝 Text-only examples:")
    for i, question in enumerate(text_questions, 1):
        print(f"\n{i}. Q: {question}")
        try:
            answer = agent.ask_question_text_only(question)
            print(f"   A: {answer[:200]}...")
        except Exception as e:
            print(f"   Error: {e}")

def example_with_image_url():
    """Example using an image URL."""
    print("\n🌐 Image URL Example")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        agent = MultimodalQAAgent()
        
        # Example with a sample image URL (you can replace this)
        image_url = "https://via.placeholder.com/400x300/0000FF/FFFFFF?text=Sample+Image"
        question = "What do you see in this image?"
        
        print(f"Image URL: {image_url}")
        print(f"Question: {question}")
        
        # This would work with a real image URL
        # For demonstration, we'll use text-only fallback
        answer = agent.ask_question_text_only(question)
        print(f"Answer: {answer[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")

def example_batch_processing():
    """Example of processing multiple questions on the same image."""
    print("\n📊 Batch Processing Example")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        agent = MultimodalQAAgent()
        
        # Multiple questions about the same (hypothetical) image
        questions = [
            "What is the main subject of this image?",
            "What colors are predominant?",
            "What is the setting or background?",
            "Are there any text elements visible?",
            "What is the overall mood or style?"
        ]
        
        results = []
        
        print("Processing multiple questions (using text-only for demo):")
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. {question}")
            try:
                answer = agent.ask_question_text_only(question)
                result = {
                    'question': question,
                    'answer': answer,
                    'success': True
                }
                print(f"   ✅ {answer[:150]}...")
            except Exception as e:
                result = {
                    'question': question,
                    'answer': None,
                    'success': False,
                    'error': str(e)
                }
                print(f"   ❌ Error: {e}")
            
            results.append(result)
        
        # Save results
        with open('examples/batch_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Results saved to: examples/batch_results.json")
        
    except Exception as e:
        print(f"Error: {e}")

def example_error_handling():
    """Example showing error handling and fallback mechanisms."""
    print("\n🛡️ Error Handling Example")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        agent = MultimodalQAAgent()
        
        # Simulate different error scenarios
        test_cases = [
            {
                'name': 'Normal text question',
                'question': 'What makes a good photograph?',
                'should_fail': False
            },
            {
                'name': 'Empty question',
                'question': '',
                'should_fail': True
            },
            {
                'name': 'Very long question',
                'question': 'What ' * 1000 + 'is this?',
                'should_fail': False  # Might work but truncated
            }
        ]
        
        for case in test_cases:
            print(f"\n🧪 Testing: {case['name']}")
            print(f"Question: {case['question'][:100]}{'...' if len(case['question']) > 100 else ''}")
            
            try:
                if case['question'].strip():
                    answer = agent.ask_question_text_only(case['question'])
                    print(f"✅ Success: {answer[:100]}...")
                else:
                    print("⚠️ Skipped empty question")
                    
            except Exception as e:
                print(f"❌ Error (expected: {case['should_fail']}): {e}")
    
    except Exception as e:
        print(f"Setup error: {e}")

def example_model_info():
    """Example showing how to get model information."""
    print("\n📋 Model Information Example")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        agent = MultimodalQAAgent()
        info = agent.get_model_info()
        
        print("🤖 Model Configuration:")
        for key, value in info.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all examples."""
    print("🎯 Multimodal QA Agent Examples")
    print("=" * 60)
    
    # Run all examples
    example_basic_usage()
    example_with_image_url()
    example_batch_processing()
    example_error_handling()
    example_model_info()
    
    print("\n" + "=" * 60)
    print("✨ All examples completed!")
    print("\n💡 To use with real images:")
    print("1. Set up your GOOGLE_API_KEY in .env file")
    print("2. Use the Streamlit app: streamlit run app.py")
    print("3. Or modify these examples with real image data")

if __name__ == "__main__":
    main()
