from dotenv import load_dotenv # Load environement variables from .env file 
import os 
from groq import Groq

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq client with the API key from the environment variables 
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# PART 1: Basic Prompt Templates 
# Define the prompt template 
def part1(topic="cats"):
    template = "Tell me a joke about {topic}."
    message = [{
        "role": "user",
        "content": template.format(topic=topic)
    }]
    response = groq_client.chat.completions.create(
        model= "llama3-70b-8192",
        messages=message,
        temperature=0.7,
        
    )
    print("\n-----Part 1: Basic Prompt Templates-----\n")
    print(f"Prompt: {template.format(topic=topic)}")
    print(f"Response: {response.choices[0].message.content}\n")
    
# Multiple Prompt Templates 
def part2(adjective="funny", topic="cats"):
    template = """ You are a helpful assistant.
Human: Tell me a {adjective} story about {topic}.
assistant:    
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": template.format(
            adjective=adjective, 
            topic=topic
        )}
    ]
    
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7,
    )
    print("\n-----Part 2: Multiple Prompt Templates-----\n")
    print(f"Prompt: {template.format(adjective=adjective, topic=topic)}")
    print(f"Response: {response.choices[0].message.content}\n")
    
if __name__ == "__main__":
    part1()    
