from flask import Flask, render_template, request, jsonify
import openai
import pywhatkit
import datetime
import webbrowser
import os
import pyttsx3
import time

app = Flask(__name__)

# OpenRouter API Key and Base
openai.api_key = ""
openai.api_base = ""

# Text-to-speech engine initialization
engine = pyttsx3.init()

# Function to get response from OpenRouter
def get_chat_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

# Function to handle text-to-speech, ensuring it works for long responses
def speak_long_response(response):
    # Split the response into smaller chunks if it is too long
    chunk_size = 200  # You can adjust this based on your preference
    chunks = [response[i:i + chunk_size] for i in range(0, len(response), chunk_size)]

    # Speak each chunk
    for chunk in chunks:
        engine.say(chunk)
        engine.runAndWait()
        time.sleep(1)  # Optional: Add a small delay between chunks

# Function to open YouTube and play a song directly
def play_youtube_video(song_name):
    # Construct YouTube search URL
    video_url = f"https://www.youtube.com/results?search_query={song_name}"
    # Open the first video from the search results
    webbrowser.open(video_url)

# Function to perform OS-level tasks (like opening applications)
def perform_os_action(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "play" in command:
        song = command.replace("play", "").strip()
        if song:
            pywhatkit.playonyt(song)  # This will play the song directly on YouTube
            return f"Playing {song} on YouTube."
        else:
            return "Please specify a song to play."
    elif "open calculator" in command:
        os.system("calc")  # Opens calculator on Windows OS
        return "Opening Calculator."
    else:
        return "Command not recognized."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"].lower()

        # Step 1: Check for sensitive mental health keywords
        sensitive_keywords = ["suicide", "kill myself", "end my life", "depressed", "hopeless", "worthless"]
        if any(word in query for word in sensitive_keywords):
            response = (
                "I'm really sorry you're feeling this way. You're not alone. "
                "Please talk to a trusted person, or contact a mental health professional. "
                "Helpline: iCall - 9152987821 or visit befrienders.org."
            )

            # Respond with voice and written text
            speak_long_response("Please know that your life matters. You're not alone. Help is available.")
            return jsonify({'response': response})

        # Step 2: Try performing OS-level command
        response = perform_os_action(query)

        # Step 3: If no special command matched, use OpenRouter AI
        if response == "Command not recognized.":
            response = get_chat_response(query)

        # Step 4: Speak and return the response
        speak_long_response(response)
        return jsonify({'response': response})

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
