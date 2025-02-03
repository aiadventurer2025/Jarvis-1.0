# Import necessary libraries
import cohere  # Import the Cohere library for AI services.
from rich import print  # Import the Rich library to enhance terminal outputs.
from dotenv import dotenv_values  # Import dotenv to load environment variables from a .env file.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("Cohere_API_Key")

# Create a Cohere client using the provided API key.
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized function keywords for task categorization.
funcs = [
    "General", "Realtime", "SimpleAutomation", "ComplexAutomation", 
    "Schedule", "ScreenSharing", "CameraSharing", "Crawl", "Exit"
]

# Initialize an empty list to store user messages.
messages = []

# Define the preamble that guides the AI model on how to categorize queries.
preamble = """
You are a highly accurate Decision-Making Model that categorizes user queries into specific functional categories.
Your task is to decide the type of query based on the following categories:

1. **General**: Use this category if the query can be answered by an LLM without requiring external or up-to-date data. Examples:
   - "What is Python?"
   - "Explain photosynthesis."
   - "Tell me a joke."

2. **Realtime**: Use this category if the query requires real-time or up-to-date information. Examples:
   - "What is the stock price of Tesla?"
   - "Who is Elon Musk"
   - "Who is the president of america"
   - "What is today's news?"
   - "Top AI news"
   - "What is the weather in Delhi?"

3. **SimpleAutomation**: Use this category if the query involves performing simple actions. Examples:
   - "Open YouTube."
   - "Play music."
   - "Close Chrome."
   - "scroll down"
   - "forward"
   - "Search for Python tutorials on Google."

*** If the user says goodbye or wants to end the conversation, respond with 'exit'. Example:
   - "Bye." → 'exit'

*** If you cannot determine, default to 'General'.

"""

# Define a chat history with predefined user-chatbot interactions for context.
chatHistory = [
    {"role": "User", "message": "What is Python?"},
    {"role": "Chatbot", "message": "General"},
    {"role": "User", "message": "Who is Elon Musk?"},
    {"role": "Chatbot", "message": "Realtime"},
    {"role": "User", "message": "Open YouTube"},
    {"role": "Chatbot", "message": "SimpleAutomation"},
    {"role": "User", "message": "Bye."},
    {"role": "Chatbot", "message": "Exit"}
]

# Define the main function for decision-making on queries.
def FirstLayerDMX(prompt: str = "test"):
    # Add the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model='command-r-plus',  # Specify the Cohere model to use.
        message=prompt,         # Pass the user's query.
        temperature=0.7,        # Set the creativity level of the model.
        chat_history=chatHistory,  # Provide the predefined chat history for context.
        prompt_truncation='OFF',  # Ensure the prompt is not truncated.
        connectors=[], # additional connectors are used.
        preamble=preamble # Pass the detailed instruction preamble.
    )

    # Initialize an empty string to store the generated response.
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text # Append generated text to the response.

    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", "")
    response = response.split(",")

    # Strip leading and trailing whitespaces from each task.
    response = [i.strip() for i in response]

    # Initialize an empty list to filter valid tasks.
    temp = []

    # Filter the tasks based on recognized function keywords.
    for task in response:
        for func in funcs:
            if task.startswith(func):
                # Extract only the category (e.g., "general" instead of "general (query)").
                temp.append(task.split(" ")[0]) # Add valid categories to the filtered list.

    # Update the response with the filtered list of categories.
    response = temp

    if "(query)" in response:
        newresponse = FirstLayerDMX(prompt=prompt)
        return newresponse
    else:
        return response
    
