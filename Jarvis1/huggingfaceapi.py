from huggingface_hub import InferenceClient

# Create an InferenceClient with your API key
client = InferenceClient(api_key="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")

# Messages include a system message and a user message
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant named ARJ's jarvis u give very short and efficient answers and do not bold any text."
    },
    {
        "role": "user",
        "content": "introduce urself"
    }
]

# Call the model for text completion with a max token limit of 10
stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",  # Using the chosen model
    messages=messages,  # Including both system and user messages
    max_tokens=10,  # Set the maximum number of tokens to generate
    stream=True  # Streaming the result in real-time
)

# Print the generated response as it's streamed
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
