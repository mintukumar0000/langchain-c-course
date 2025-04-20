from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configuration - Centralize model parameters
MODEL_CONFIG = {
    "model": "llama3-70b-8192",
    "temperature": 0.7,
    "max_tokens": 1024
}

def format_base_prompt(product_name: str) -> list:
    """Create initial feature extraction prompt
    Replaces: ChatPromptTemplate.from_messages for base features"""
    return [
        {
            "role": "system",
            "content": "You are an expert product reviewer."
        },
        {
            "role": "user",
            "content": f"List the main features of the product {product_name}."
        }
    ]

def analyze_aspect(features: str, aspect_type: str) -> str:
    """Generic analyzer for both pros and cons
    Replaces: pros_branch_chain and cons_branch_chain"""
    try:
        messages = [
            {
                "role": "system",
                "content": "You are an expert product reviewer."
            },
            {
                "role": "user",
                "content": f"Given these features: {features}, list the {aspect_type} of these features."
            }
        ]
        
        response = groq_client.chat.completions.create(
            messages=messages,
            **MODEL_CONFIG
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing {aspect_type}: {str(e)}"

def generate_product_review(product_name: str) -> str:
    """Main execution flow combining all components
    Replaces: LCEL chain structure"""
    try:
        # Step 1: Get base features
        base_messages = format_base_prompt(product_name)
        features_response = groq_client.chat.completions.create(
            messages=base_messages,
            **MODEL_CONFIG
        )
        features = features_response.choices[0].message.content
        
        # Step 2: Parallel analysis of pros and cons
        pros = analyze_aspect(features, "pros")
        cons = analyze_aspect(features, "cons")
        
        # Step 3: Combine results
        return f"Product: {product_name}\n\nFeatures:\n{features}\n\nPros:\n{pros}\n\nCons:\n{cons}"
    
    except Exception as e:
        return f"Review generation failed: {str(e)}"

# Execute the review generation
result = generate_product_review("MacBook Pro")
print(result)