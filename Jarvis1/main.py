import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as py3
import requests
from huggingface_hub import InferenceClient
import music_lib
import cohere
from gtts import gTTS
import pygame
import os
from elevenlabs import ElevenLabs

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = py3.init()
news_api = "68fc7be47d7apikey62c0b1" #myapi
# news_api = "d093053d72bc40248998159804e0e67d" #harry's api

# Get the user's name manually
username = input("Enter your name: ")

# Set voice properties
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Default to first voice
engine.setProperty("rate", 130)  # Set speech rate

# Function to speak text
####################################### pyttsx #################################################
def speak1(text):
    engine.say(text)
    engine.runAndWait()
########################################################################################

####################################### gtts #################################################
def speak2(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check every 10ms if music is still playing

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
###########################################################################################


####################################### 11 labs #################################################
client = ElevenLabs(api_key="sk_apikey27")

def speak(text):
    try:
        # Generate speech using 11 Labs
        audio = client.generate(
            text=text,
            voice="Alice",  # Use your desired voice
            model="eleven_multilingual_v1"
            # voice="Muskaan",  # Use your desired voice
            # model="muskaan-casual-hindi-v1"
        )

        # Convert generator output to bytes
        audio_bytes = b"".join(audio)  # Ensures the audio data is in byte format

        # Save the audio to a temporary file
        temp_file = "tem.mp3"
        with open(temp_file, "wb") as file:
            file.write(audio_bytes)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the MP3 file
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Cleanup
        pygame.mixer.music.unload()
        os.remove(temp_file)

    except Exception as e:
        print(f"An error occurred: {e}")





#ai function
def ai_chat(command):
###################################### this is huggingface ##################################
    # # Create an InferenceClient with your API key
    # client = InferenceClient(api_key="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")

    # # Messages include a system message and a user message
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are a helpful assistant named ARJ's jarvis u give very short, efficient and correct answers and do not bold any text."
    #     },
    #     {
    #         "role": "user",
    #         "content": command
    #     }
    # ]

    # # Call the model for text completion with a max token limit of 10
    # stream = client.chat.completions.create(
    #     model="Qwen/Qwen2.5-Coder-32B-Instruct",  # Using the chosen model
    #     messages=messages,  # Including both system and user messages
    #     max_tokens=50,  # Set the maximum number of tokens to generate
    #     stream=True  # Streaming the result in real-time
    # )

    # # Print the generated response as it's streamed
    # result = ""
    # for chunk in stream:
    #     result += chunk.choices[0].delta.content
    # return result
#############################################################

####################################### this is cohere###################################
    co = cohere.ClientV2("FkNCmGQyTnET23r50QwcBP5GJML9rxMD4rNjKuLO")

    # Define the conversation with both user and assistant messages
    conversation = [
            {
            "role": "system",
            "content": "You are a helpful assistant and your name is ARJ's Chat_Bot u give very short, efficient and correct answers remember that you can be receive content in any language but you will always give response in english and do not bold any text answers should be very short."
        },
        {
            "role": "user",
            "content": command
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
    return (assistant_message)
################################################################################





# Function to process commands
def processCommand(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        wb.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        wb.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        wb.open("https://facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        wb.open("https://linkedin.com")

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = music_lib.music[song]
        speak(f"Playing {song}")
        wb.open(link)

    elif "news" in command.lower():
        try:
            # Make the request to the News API
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if articles:
                    # Loop through the articles and speak the title
                    for article in articles:
                        title = article.get('title', 'No title available')
                        print(title)
                        speak(title)
                else:
                    speak("Sorry, no news articles found.")
            else:
                speak(f"Failed to fetch news. Status code: {r.status_code}")
        except Exception as e:
            speak(f"Error fetching news: {e}")
        


    elif "exit" in command or "stop" in command or "s t o p" in command or "e x i t" in command or "bye" in command or "b y e" in command:
        speak(f"Goodbye, {username}.")
        exit(0)  # Exit the program gracefully
    else:
        # speak("Sorry, I did not understand the command.")
        #Let open ai handle the requets
        output = ai_chat(command)
        print(output)
        speak(output)

# Function to listen for wake word
def listen_for_wake_word():
    print("Listening for 'hello'...")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)  # Listen for wake word

            # Recognize speech using Google Speech Recognition
            word = recognizer.recognize_google(audio)
            print(f"Recognized word: {word}")

            if word.lower() == "hello":  # Wake word detection
                speak(f"Good evening {username}, Chat_bot is now active.")
                listen_for_commands()  # Now, listen for actual commands when "hello" is said
            else:
                print("Not a wake word. Please say 'hello' to activate Jarvis.")
        
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please say 'hello' to activate Jarvis.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")

# Function to listen for commands after wake word
def listen_for_commands():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for a command...")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)  # Listen for commands

            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            processCommand(command)  # Process the command
            
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")

# Start the program
if __name__ == "__main__":
    speak("Initializing Chatbot....")
    listen_for_wake_word()  # Start listening for the wake word

