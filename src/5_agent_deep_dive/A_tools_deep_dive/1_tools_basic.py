from dotenv import load_dotenv
import os 
from groq import Groq
import json

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq client with your API key
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define the tools 
def greet_user(name: str) -> str:
    """Greet the user with their name."""
    return f"Hello, {name}!"

def reverse_string(string: str) -> str:
    """Reverse the input string."""
    return string[::-1]

def concatenate_strings(a: str, b: str) -> str:
    """Concatenate two strings."""
    return a + b

# Tools configuration (metadata only for prompt)
tools_config = {
    "GreetUser": {
        "description": "Greets user by name. Input: single 'name' parameter",
        "args": ["name"]
    },
    "ReverseString": {
        "description": "Reverses input string. Input: single 'text' parameter",
        "args": ["text"]
    },
    "ConcatenateStrings": {
        "description": "Concatenates two strings. Input: 'a' and 'b' parameters",
        "args": ["a", "b"]
    }
}

# Actual tools implementation map
tools_implementation = {
    "GreetUser": greet_user,
    "ReverseString": reverse_string,
    "ConcatenateStrings": concatenate_strings
}

# Prompt template for the agent 
system_prompt = f"""You are a helpful assistant that can access tools.
Available Tools:
{json.dumps(tools_config, indent=2)}

Respond with JSON containing:
- "thought": your reasoning
- "tool": tool name or "direct_answer"
- "parameters": dictionary of parameters
"""

def process_query(query: str) -> str:
    """Main processing function for handling queries"""
    try:
        # First LLM call to determine tool usage
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            model="llama3-70b-8192",
            temperature=0,
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        # Parse JSON response
        decision = json.loads(response.choices[0].message.content)
        
        if decision["tool"] == "direct_answer":
            return decision["thought"]
        
        # Execute selected tool
        tool_func = tools_implementation[decision["tool"]]
        result = tool_func(**decision["parameters"])
        
        # Second LLM call to format final response
        final_response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
                {"role": "assistant", "content": json.dumps(decision)},
                {"role": "user", "content": f"Tool Result: {result}"}
            ],
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=300
        )
        
        return final_response.choices[0].message.content
        
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Test cases
if __name__ == "__main__":
    # Test 1: Greet user
    response = process_query("Greet Alice")
    print("Response for 'Greet Alice':", response)
    
    # Test 2: Reverse string
    response = process_query("Reverse the string 'hello'")
    print("Response for 'Reverse the string hello':", response)
    
    # Test 3: Concatenate strings
    response = process_query("Concatenate 'hello' and 'world'")
    print("Response for 'Concatenate hello and world':", response)