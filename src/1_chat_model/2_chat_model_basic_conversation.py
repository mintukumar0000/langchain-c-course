from dotenv import load_dotenv # Load environment variables from .env file 
import os  # Operating system interface 
from groq import Groq # Groq API client 

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq API_KEY from the environment variable 
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

# Initialize the Groq API client 
groq_client = Groq(api_key=groq_api_key)


# Define the conversation function 
class converation:
    def __init__(self, system_message=None):
        self.messages = []
        if system_message:
            self.add_system_message(system_message) # Add system message if provided
            
    def add_system_message(self, content):
        """Add a system message to the conversation."""
        self.messages.append({"role": "system", "content": content})
        
    def add_use_message(self, content):
        """Add a user message to the conversation."""
        self.messages.append({"role": "user", "content": content})
        
    def add_assistant_message(self, content):
        """ Add an assistant message to the conversation."""
        self.messages.append({"role": "assistant", "content": content})
        
    def get_messages(self):            
        """Get the conversation messages."""
        return self.messages
    
    def clear(self):
        """Clear the conversation messages."""
        self.messages = []
        
# Creating the new conversation with system messages
converation = converation(
    system_message="You are a helpful assistant. You can answer questions and provide information on various topics."
    
    
)   
def get_model_response(messages):
    """ Send the conversation messages to the model and get the response."""
    response = groq_client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192", # Specify the model to use
    )     
    return response.choices[0].message.content # Return the assistant's response

# Start the conversation loop
print("Start conversation with the model. Type 'exit' to end the conversation")
print()


while True:
    # Get user input 
    user_input = input("You: ")
    
    # Check if the user wants to exit the conversation
    if user_input.lower() == "exit":
        print("Ending conversation.")
        print("Goodbye!")
        break
    
    # Add user message to the conversation
    converation.add_use_message(user_input)
    
    # Get the model response 
    print("Assistant is thinking...")
    assistant_response = get_model_response(converation.get_messages())
    
    # Add assistant message to the conversation
    converation.add_assistant_message(assistant_response)
    
    
    # Print the assistant's response
    print(f"Assistant: {assistant_response}")
    print()