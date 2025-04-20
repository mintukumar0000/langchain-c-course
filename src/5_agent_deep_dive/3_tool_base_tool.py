import os
import json
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

# Load environment variables from .env
load_dotenv()

# Initialize clients with API keys
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Define tool functions ========================================================
def simple_search(query: str) -> str:
    """Search web using Tavily API"""
    results = tavily_client.search(query=query)
    return f"Search results for '{query}':\n{json.dumps(results, indent=2)}"

def multiply_numbers(x: float, y: float) -> str:
    """Multiply two numbers"""
    result = x * y
    return f"{x} multiplied by {y} equals {result}"

# Tools configuration =========================================================
tools = {
    "simple_search": {
        "func": simple_search,
        "description": "Search web for current information",
        "args": ["query"]
    },
    "multiply_numbers": {
        "func": multiply_numbers,
        "description": "Multiply two numbers",
        "args": ["x", "y"]
    }
}

# System prompt template =======================================================
system_prompt = f"""You are an AI assistant with access to tools. Follow these steps:
1. Analyze the user's request
2. Choose appropriate tool (or respond directly)
3. Format response as JSON with:
{{
    "thought": "your reasoning",
    "tool": "tool_name or 'direct_answer'",
    "parameters": {{}}
}}

Available Tools:
{json.dumps({name: {k: v for k, v in desc.items() if k != 'func'} for name, desc in tools.items()}, indent=2)}"""

def process_query(query: str) -> str:
    """Handle query processing with error handling"""
    try:
        # First call - tool selection
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
        
        decision = json.loads(response.choices[0].message.content)
        
        # Direct answer case
        if decision["tool"] == "direct_answer":
            return decision["thought"]
        
        # Tool execution
        tool = tools[decision["tool"]]
        result = tool["func"](**decision["parameters"])
        
        # Second call - format final response
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
        return f"Error: {str(e)}"

# Test cases ===================================================================
if __name__ == "__main__":
    print("Testing search tool:")
    response = process_query("Search for Apple Intelligence")
    print("Response:", response)
    
    print("\nTesting multiplication tool:")
    response = process_query("Multiply 10 and 20")
    print("Response:", response)