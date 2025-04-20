from dotenv import load_dotenv # Load environment variables from .env file 
import os 
from groq import Groq # Impot the groq library

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq client with the API key from the environment variables
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Initialize the Groq client with the API key

# Define the prompt template equivalent to the one in the chain
def create_groq_prompt(topic:str, jock_count:int) -> list:
    """Create a prompt for the Groq API."""
    return [
        {
            "role" : "system",
            "content": f"You are a comedian who tells {jock_count} jokes about {topic}."
            
        },
        {
            "role" : "user",
            "content": f"Tell me {jock_count} jokes about {topic}."
        }
    ]
# Define the model invocation function
def invoke_model(messages: list) -> dict:
    """Invoke the model with the provided messages."""
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7,
        max_tokens=1024
    ) 
    return response  # <-- Add this line

# Define the Output parser function equivalent to the one in the chain
def parse_output(response: dict) -> str:
    """Parse the output from the model respone."""
    return response.choices[0].message.content # Return the content of the responsse


# Create equivalent of RunnableSequence
def groq_chain(topic:str, jock_count:int) -> str:
    """Create a chain of operations to get the model response."""
    formatted_prompt = create_groq_prompt(topic, jock_count) # Create the formatted prompt
    model_response = invoke_model(formatted_prompt) # Invoke the model with the formatted prompt
    return parse_output(model_response) # Parse and return the output from the model response

# Execute the chain
response = groq_chain("lawyers", 3)

print(response)