import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from google import genai


# recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="Your_ApI_Key"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save('temp.mp3')


    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    # Wait until song finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = genai.Client(api_key="Your_API_KEY")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"You are Jarvis, a smart assistant. Answer shortly. User said: {command}"
    )
    
    return response.text

    



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open github" in c.lower():
        webbrowser.open("https://www.github.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")

    
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    
    
    elif "news" in c.lower():

        speak("Fetching latest news")

        url = f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={newsapi}"

        r = requests.get(url)

        if r.status_code != 200:
            speak("Network error")
            return

        data = r.json()

        if data.get("status") != "ok":
            print("API error:", data)
            speak("News service error")
            return

        articles = data.get("articles", [])

        if not articles:
            speak("No news found")
            print("No articles returned")
            return

        speak("Here are the top headlines")

        for article in articles[:5]:

            title = article.get("title")

            if title:
                print(title)
                speak(title)
    else:
        output=aiProcess(c)
        speak(output)
            

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    # Listen for the wake word Jarvis

    while True:
        r=sr.Recognizer()
        
        print("Recoginizing.....")
        try:
            with sr.Microphone() as source:
                print("Listening......")
                audio = r.listen(source, timeout=4,phrase_time_limit=3)

            word=r.recognize_google(audio)
            if(word.lower() =="jarvis"):
                speak("Ya")
                
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated....")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)
                    processCommand(command)


        except Exception as e:
            print("Error;{0}".format(e))


    
