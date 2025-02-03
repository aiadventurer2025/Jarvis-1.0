from googlesearch import search
from groq import Groq  
from json import load, dump  
import datetime  
import os  
from dotenv import dotenv_values  

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("Groq_API_Key")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system message for the chatbot.
System = f"""I am {Username} address me as sir, and you are {Assistantname}, an intelligent AI assistant with real-time access to the internet.  

Instructions:
    1. Analyze the extracted data.
    2. Provide only the specific information the user is asking for.
    3. Keep the response concise and relevant.
    4. Provide explanations or examples **only when I ask**.

Examples (Don't use any data from examples): 
    user : what is valuation of Nvidia 
    output : $3.05 trillion
    user : Top AI NEWS
    output: Recent AI NEWS are
        1.OpenAI has unveiled Operator, a tool that integrates seamlessly with web browsers to perform tasks autonomously.
        2.DeepSeek is grappling with service disruptions and restricting new account sign-ups to combat what it describes as “large-scale malicious attacks.”
        ....
"""  

# Function to get the current date in YYYY-MM-DD format.
def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Function to get the path for the chat log file based on the current date.
def get_chat_log_path():
    date = get_current_date()
    return os.path.join("Backend/Data", "ChatHistory.json")

# Function to load chat logs for the current date.
def load_chat_log():
    chat_log_path = get_chat_log_path()
    if os.path.exists(chat_log_path):
        with open(chat_log_path, "r") as f:
            return load(f)
    return []

# Function to save chat logs for the current date.
def save_chat_log(messages):
    chat_log_path = get_chat_log_path()
    os.makedirs("Backend/Data", exist_ok=True)  # Create the Data directory if it doesn't exist.
    with open(chat_log_path, "w") as f:
        dump(messages, f, indent=4)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    
    Answer += "[end]"
    
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [{"role": "system", "content": System}]

# Function to get real-time information like the current date and time.
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot

    # Load the chat log for the current date.
    messages = load_chat_log()

    # Append the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    Answer = ""

    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s", "")

    # Append the chatbot's response to the messages list.
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log for the current date.
    save_chat_log(messages)

    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()

    return AnswerModifier(Answer=Answer)

