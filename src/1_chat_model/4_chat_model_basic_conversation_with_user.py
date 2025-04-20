from dotenv import load_dotenv
import os 
from groq import Groq 

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

groq = Groq(api_key=groq_api_key)

# Corrected role to lowercase
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Exiting the chat.")
        break
    
    # Corrected role to lowercase
    chat_history.append({"role": "user", "content": user_input})
    
    response = groq.chat.completions.create(
        messages=chat_history, 
        model="llama3-70b-8192",
        temperature=0.7,
        max_tokens=1024
    )
    
    ai_response = response.choices[0].message.content
    # Corrected role to lowercase
    chat_history.append({"role": "assistant", "content": ai_response})
    
    print(f"AI: {ai_response}")

print("\n--- Message History ---")
for message in chat_history:
    print(f"{message['role']}: {message['content']}")