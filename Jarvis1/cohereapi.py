import cohere

co = cohere.ClientV2("api")

# Define the conversation with both user and assistant messages
conversation = [
        {
        "role": "system",
        "content": "You are a helpful assistant and your name is ARJ's Chat_bot u give very short answers and do not bold any text."
    },
    {
        "role": "user",
        "content": "what's your name"
    }
]

# Send the conversation to the API
response = co.chat(
    model="command-r", 
    messages=conversation
)

# Extract only the assistant's response
assistant_message = response.message.content[0].text

# Print the assistant's message
print(assistant_message)

