"""
Sample test cases for the Multimodal QA Agent.
This script demonstrates testing with actual image-question pairs.
"""

import os
import base64
import json
from datetime import datetime
from dotenv import load_dotenv
from multimodal_agent import MultimodalQAAgent
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def create_sample_images():
    """Create sample images for testing."""
    samples = []
    
    # Sample 1: Product image simulation
    img1 = Image.new('RGB', (400, 300), color='white')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([50, 50, 350, 250], fill='blue', outline='black', width=3)
    draw1.text((80, 140), "PRODUCT", fill='white')
    buffer1 = BytesIO()
    img1.save(buffer1, format='JPEG')
    
    samples.append({
        'name': 'product_sample',
        'image_data': base64.b64encode(buffer1.getvalue()).decode(),
        'questions': [
            "What product is shown in this image?",
            "What color is the product?",
            "Describe the overall design and layout"
        ]
    })
    
    # Sample 2: Chart simulation
    img2 = Image.new('RGB', (400, 300), color='white')
    draw2 = ImageDraw.Draw(img2)
    # Simple bar chart
    bars = [(50, 200, 80, 250), (100, 150, 130, 250), (150, 180, 180, 250)]
    colors = ['red', 'green', 'blue']
    for bar, color in zip(bars, colors):
        draw2.rectangle(bar, fill=color)
    draw2.text((200, 50), "Sample Chart", fill='black')
    buffer2 = BytesIO()
    img2.save(buffer2, format='JPEG')
    
    samples.append({
        'name': 'chart_sample',
        'image_data': base64.b64encode(buffer2.getvalue()).decode(),
        'questions': [
            "What type of chart is this?",
            "What trends can you identify?",
            "How many data points are shown?"
        ]
    })
    
    # Sample 3: Scene simulation
    img3 = Image.new('RGB', (400, 300), color='lightblue')
    draw3 = ImageDraw.Draw(img3)
    # Simple landscape
    draw3.rectangle([0, 200, 400, 300], fill='green')  # Ground
    draw3.ellipse([50, 50, 100, 100], fill='yellow')   # Sun
    draw3.rectangle([150, 150, 200, 200], fill='brown') # Tree trunk
    draw3.ellipse([120, 100, 230, 180], fill='darkgreen') # Tree top
    buffer3 = BytesIO()
    img3.save(buffer3, format='JPEG')
    
    samples.append({
        'name': 'landscape_sample',
        'image_data': base64.b64encode(buffer3.getvalue()).decode(),
        'questions': [
            "Describe the setting and atmosphere of this image",
            "What objects can you identify?",
            "What is the weather like in this scene?"
        ]
    })
    
    return samples

def run_sample_tests():
    """Run tests with sample images and questions."""
    load_dotenv()
    
    try:
        agent = MultimodalQAAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Create sample images
    samples = create_sample_images()
    print(f"📸 Created {len(samples)} sample images")
    
    # Test results storage
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': agent.get_model_info(),
        'results': []
    }
    
    # Run tests for each sample
    for i, sample in enumerate(samples, 1):
        print(f"\n🧪 Testing Sample {i}: {sample['name']}")
        sample_results = {
            'sample_name': sample['name'],
            'questions_and_answers': []
        }
        
        for j, question in enumerate(sample['questions'], 1):
            print(f"  Question {j}: {question}")
            
            try:
                # Try vision model first
                answer = agent.ask_question(question, sample['image_data'])
                print(f"  ✅ Vision Answer: {answer[:100]}...")
                
                sample_results['questions_and_answers'].append({
                    'question': question,
                    'answer': answer,
                    'model_used': 'gemini-pro-vision',
                    'success': True
                })
                
            except Exception as e:
                print(f"  ⚠️ Vision model failed: {e}")
                
                # Try fallback
                try:
                    fallback_answer = agent.ask_question_text_only(question)
                    print(f"  🔄 Fallback Answer: {fallback_answer[:100]}...")
                    
                    sample_results['questions_and_answers'].append({
                        'question': question,
                        'answer': fallback_answer,
                        'model_used': 'gemini-pro (fallback)',
                        'success': True,
                        'vision_error': str(e)
                    })
                    
                except Exception as fallback_e:
                    print(f"  ❌ Fallback also failed: {fallback_e}")
                    
                    sample_results['questions_and_answers'].append({
                        'question': question,
                        'answer': None,
                        'model_used': None,
                        'success': False,
                        'vision_error': str(e),
                        'fallback_error': str(fallback_e)
                    })
        
        test_results['results'].append(sample_results)
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📊 Test Results Summary:")
    print(f"Total samples tested: {len(samples)}")
    
    total_questions = sum(len(sample['questions']) for sample in samples)
    successful_answers = sum(
        sum(1 for qa in result['questions_and_answers'] if qa['success'])
        for result in test_results['results']
    )
    
    print(f"Total questions: {total_questions}")
    print(f"Successful answers: {successful_answers}")
    print(f"Success rate: {successful_answers/total_questions*100:.1f}%")
    print(f"Results saved to: test_results.json")

if __name__ == "__main__":
    run_sample_tests()
