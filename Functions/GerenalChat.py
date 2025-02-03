from groq import Groq  
from json import load, dump  
import datetime  
import os  
from dotenv import dotenv_values  

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")  

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("Groq_API_Key")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, and you are {Assistantname}, an intelligent AI assistant.  

- Only give short and direct answers.   
- Avoid unnecessary details or extra information.  
- Keep responses natural and to the point.  
- Do not mention your training data or provide system notes.

Examples (Don't use any data from examples): 
    user : Full Form of LLM
    output : Large language models 
    user : Explain LLM
    output: An LLM (Large Language Model) is an AI program that understands and generates text using deep learning, specifically transformer models. Trained on vast datasets, often sourced from the internet, LLMs learn language patterns and structures. Their performance depends on data quality, and they can be fine-tuned for specific tasks like answering questions or translating languages.
        
"""  

SystemChatBot = [{"role": "system", "content": System}]

# Function to get the path for the chat log file.
def get_chat_log_path():
    return os.path.join("Backend/Data", "ChatHistory.json")

# Function to load chat logs.
def load_chat_log():
    chat_log_path = get_chat_log_path()
    if os.path.exists(chat_log_path):
        with open(chat_log_path, "r") as f:
            return load(f)
    return []

# Function to save chat logs.
def save_chat_log(messages):
    chat_log_path = get_chat_log_path()
    os.makedirs("Backend/Data", exist_ok=True)  # Create the Data directory if it doesn't exist.
    with open(chat_log_path, "w") as f:
        dump(messages, f, indent=4)

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  
    non_empty_lines = [line for line in lines if line.strip()]  
    modified_answer = '\n'.join(non_empty_lines)  
    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """
    try:
        # Load the chat log for the current date.
        messages = load_chat_log()

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  
            messages=[{"role": "system", "content": System}] + messages,  
            max_tokens=1024,  
            temperature=0.0,  
            top_p=1,  
            stream=True,  
            stop=None  
        )

        Answer = ""  
        for chunk in completion:
            if chunk.choices[0].delta.content:  
                Answer += chunk.choices[0].delta.content  

        Answer = Answer.replace("</s>", "")  

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log for the current date.
        save_chat_log(messages)

        # Return the formatted response.
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        save_chat_log([])  # Reset the chat log for the current date.
        return ChatBot(Query)  # Retry the query after resetting the log.

