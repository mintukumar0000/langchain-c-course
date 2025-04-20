from dotenv import load_dotenv # Load environment variables from .env file 
import os 
from groq import Groq # Import the Groq library
from datetime import datetime # Import datetime for timestamping
import json # Import json for handling JSON data
from wikipedia import summary # Import summary function from wikipedia


# Load environment variables from .env file 
load_dotenv()

# Initialize the groq client with the API key from the environment variables
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Initialize the Groq client with the API key 


# Define the tools function
def get_current_time():
    """Get the current time."""
    return datetime.now().strftime("%I:%M %p") # Return the current time in HH:MM AM/PM format 

def get_wikipedia_summary(query):
    """ Search the wikipedia and return the summary."""
    try:
        return summary(query, sentences=2) # Return the summary of the query
    except:
        return "No, relevant information found in Wikipedia." # Return the error message if no relevant information is found
    
# Tools configuration
tools = [
    {
        "name": "Time",
        "func": get_current_time,
        "description": "Get the current time in HH:MM AM/PM format."
    },
    {
        "name": "Wikipedia Summary",
        "func": get_wikipedia_summary,
        "description": "Fetch a summary from Wikipedia based on a query."
    }
]
# Structure the chat prompt templates 
react_prompt = """You are an AI assistant that can access tools. Maintain conversation history and context.

Available Tools:
{tools}

Chat History:
{chat_history}

Current Interaction:
User: {input}

Response Format (JSON):
{{
    "thought": "your reasoning process",
    "action": "tool_name or final_answer",
    "action_input": "input_for_tool",
    "observation": "tool_result (if using tool)"
}}"""
# Memory management
chat_history = [] # List to store chat history

def update_memory(role, content):
    """Store messages in memory with role-based formatting"""
    chat_history.append({
        "role": "system" if role == "system" else "user" if role == "user" else "assistant",
        "content": content
    })
    
# Initialize with the system message 
update_memory("system", "You are a helpful assistant. You can answer questions and provide information on various topics.")

# Agent execution logic
def execute_agent(user_input):
    """Handle the agent execution with ReAct pattern and return the full process"""
    try:
        # Format prompt with current context
        formatted_prompt = react_prompt.format(
            tools="\n".join([f"{t['name']}: {t['description']}" for t in tools]),
            chat_history="\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history]),
            input=user_input
        )
        # Get LLM initial response
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": formatted_prompt}],
            model="llama3-70b-8192",
            temperature=0.3,
            max_tokens=500
        )
        # Parse json response
        agent_response = json.loads(response.choices[0].message.content)
        
        
        # Handle tool usage
        if agent_response["action"] != "final_answer":
            for tool in tools:
                if tool["name"] == agent_response["action"]:
                    observation = tool["func"](agent_response["action_input"])
                    agent_response["observation"] = observation
                    break
            
            # Create follow-up prompt with tool result
            follow_up_prompt = f"Tool Result: {agent_response['observation']}\nGenerate final answer:"
            final_response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": follow_up_prompt}],
                model="llama3-70b-8192",
                temperature=0.3,
                max_tokens=300
            )
            return final_response.choices[0].message.content
        
        return agent_response["observation"]
    except Exception as e:
        return f"Error processing request: {str(e)}" # Return the error message if any error occurs
    
    
# Chat interface
print("Chat started. Type 'exit' to end the chat.\n")
while True:
    user_input = input("\nUser: ")
    if user_input.lower() == "exit":
        break
    
    # Add user message to memory
    update_memory("user", user_input)
    
    # Get agent response
    bot_response = execute_agent(user_input)
    
    # Add bot response to memory
    update_memory("assistant", bot_response)
    
    print(f"Bot: {bot_response}")