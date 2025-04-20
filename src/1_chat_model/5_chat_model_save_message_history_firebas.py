from dotenv import load_dotenv
import os 
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from groq import Groq
from langchain_core.messages import HumanMessage, AIMessage  # New import

# Load environment variables
load_dotenv()

# Initialize services
PROJECT_ID = "chat-history-demo-f7b63"
SESSION_ID = "user_session_1"
COLLECTION_NAME = "chat_history"

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Firestore client
client = firestore.Client(project=PROJECT_ID)
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,
)

# New: Display previous conversation on startup
print("\n=== Loading Previous Conversation ===")
if len(chat_history.messages) > 0:
    for msg in chat_history.messages:
        if isinstance(msg, HumanMessage):
            print(f"You: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"AI: {msg.content}")
    print("===================================\n")
else:
    print("No previous conversation found\n")

# Configure model
MODEL_NAME = "llama3-70b-8192"

def get_groq_response(messages):
    """Get response from Groq API"""
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def format_firestore_messages():
    """Convert Firestore messages to Groq format"""
    return [
        {
            "role": "system" if msg.type == "system" else "user" if msg.type == "human" else "assistant",
            "content": msg.content
        } 
        for msg in chat_history.messages
    ]

print("Start chatting with AI. Type 'exit' to end the chat.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":    
        break
    
    # Add user message to history
    chat_history.add_user_message(user_input)
    
    # Get formatted messages
    formatted_messages = format_firestore_messages()
    
    # Get response
    ai_response = get_groq_response(formatted_messages)
    
    # Add AI response
    chat_history.add_ai_message(ai_response)
    
    print(f"AI: {ai_response}\n")

print("\nChat session saved to Firestore.")