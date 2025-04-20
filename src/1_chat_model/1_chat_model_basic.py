from dotenv import load_dotenv # Load environment variables from .env file
import os
from groq import Groq # Import the Groq library


# Load environment variables from .env file
# Ensure you have a .env file with your API key
load_dotenv()


# Initialize the Groq client with your API key
groq_api_key = os.getenv("GROQ_API_KEY") # Fetch the API key from environment variables

# Check if the API key is set
# IF not, raise an error
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file") # Raise an error if the API key is not set 

groq_client = Groq(api_key=groq_api_key) # Initialize the Groq client with the API key

# Using the currently supported llama3-70b-8192 model
response = groq_client.chat.completions.create( # Create a chat completion
                                               # Send the request to the Groq API
    messages=[
        {
            "role": "user", # The role of the message sender
            "content": "What is 81 divided by 9?" # The content of the message
        }
    ],
    model="llama3-70b-8192"  # The model to use for the chat completion
)

print("Content only:")
print(response.choices[0].message.content) # Print the content of the response