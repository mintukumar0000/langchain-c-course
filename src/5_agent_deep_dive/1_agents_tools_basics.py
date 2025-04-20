from dotenv import load_dotenv # Load environment variables from .env file 
import os 
from groq import Groq # Import the Groq library
from datetime import datetime # Import datetime for timestamping 

# Load environment variables from .env file 
load_dotenv()

# Initialize the Groq client with your API key 
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY") ) # Fetch the API key from environment varaibles 

# Define the tools 
def get_current_time(*args, **kwargs):
    """Tool function that returns the current time in HH:MM:SS format.
    Example usage: "03:45:12"
    """
    return datetime.now().strftime("%H:%M:%S") # Return the current time in HH:MM:SS format

# Define the available tools 
tools = [{
    "name" : "Time", # The name of the tool
    "func" : get_current_time, # The function to call when the tool is used
    "description" : "Get the current time in HH:MM:SS format." # The description of the tool  
}]

# Define the ReAct prompt template 
react_prompt = """ Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad} 
"""

# Agent execution logic

def run_agent(query: str):
    """
    Executes the agent loop with ReAct pattern and returns full process
    """
    full_process = []  # Track complete chain of thoughts
    max_steps = 3
    step = 0
    scratchpad = ""
    
    while step < max_steps:
        formatted_prompt = react_prompt.format(
            tools="\n".join([f"{t['name']}: {t['description']}" for t in tools]),
            tool_names=", ".join([t["name"] for t in tools]),
            input=query,
            agent_scratchpad=scratchpad
        )
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": formatted_prompt}],
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=500
        )
        
        llm_output = response.choices[0].message.content
        scratchpad += llm_output
        full_process.append(llm_output)  # Store complete output

        if "Final Answer:" in llm_output:
            return {
                "process": "\n".join(full_process),
                "answer": llm_output.split("Final Answer:")[-1].strip()
            }

        if "Action:" in llm_output and "Action Input:" in llm_output:
            action = llm_output.split("Action:")[1].split("Action Input:")[0].strip()
            action_input = llm_output.split("Action Input:")[1].split("\n")[0].strip()
            
            for tool in tools:
                if tool["name"] == action:
                    observation = tool["func"](action_input)
                    scratchpad += f"\nObservation: {observation}\nThought:"
                    full_process.append(f"Observation: {observation}")  # Add observation
                    break
        
        step += 1
        
    return {
        "process": "\n".join(full_process),
        "answer": "Maximum steps reached without final answer"
    }

# Execute and print formatted output ===========================================
if __name__ == "__main__":
    result = run_agent("What time is it?")
    
    print("\n> Entering new AgentExecutor chain...")
    print(result["process"])
    print("\nFinal Answer:", result["answer"])