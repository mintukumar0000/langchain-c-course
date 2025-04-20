from dotenv import load_dotenv # Load environment variables from .env file 
import os
from groq import Groq # Groq API client

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq Client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
if not groq_client.api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")


# Define the conversation function
def create_groq_prompt(topic:str, jock_count:int) -> list:
    """Create a prompt for the Groq API."""
    return [
        {
            "role" : "system",
            "content" : f"You are a comedian who tells {jock_count} jokes about {topic}."
        },
        {
            "role" : "user",
            "content" : f"Tell me {jock_count} jokes about {topic}."
        }
    ]
    
# Create the complete prompt chain
def groq_chain(topic:str, jock_count:int) -> list:
    # Create formatted prompt
    message = create_groq_prompt(topic, jock_count)
    
    
    # Get the response from the Groq API
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=message,
        temperature=0.7,
        max_tokens=1024
    )    
    
    return response.choices[0].message.content

# Run the chain
result = groq_chain(topic="lawyers", jock_count=3)

# Output the result
print("Granted Jocks: ", result)
