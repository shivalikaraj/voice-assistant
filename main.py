from ai_client import ask_ai
import musicLibrary
import feedparser
import os
import requests
import datetime
import win32com.client
import webbrowser
import speech_recognition as sr


# CONFIGURATION

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NOTES_FILE = "notes.txt"

WAITING_FOR_CITY = "waiting_for_city"
WAITING_FOR_NOTE = "waiting_for_note"

STATE = {
    WAITING_FOR_CITY: False,
    WAITING_FOR_NOTE: False,
}

if not WEATHER_API_KEY:
    print("Warning: Weather API key not found.")


# SPEECH SETUP

r = sr.Recognizer()

speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()
speaker.Voice = voices.Item(1)  # female voice

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)


# SPEAK FUNCTION

def speak(text):
    speaker.Speak(text)

# LISTEN FUNCTION


def listen(timeout=None, phrase_time_limit=None):
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        return r.recognize_google(audio)

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print("Listen error:", e)
        return ""


# NEWS FUNCTION

def say_news():
    speak("Here are the latest news headlines")

    feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")

    for i, entry in enumerate(feed.entries[:5]):
        speak(f"News {i + 1}. {entry.title}")


# WEATHER FUNCTION

def say_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["cod"] != 200:
            speak("I could not find that city.")
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(
            f"The weather in {city} is {description} with a temperature of {temp} degree Celsius.")

    except Exception:
        speak("Sorry, I could not fetch the weather.")


# NOTES FUNCTIONS

def save_note(text):
    with open(NOTES_FILE, "a") as f:
        f.write(text + "\n")
    speak("Note saved.")


def read_notes():
    if not os.path.exists(NOTES_FILE):
        speak("You have no notes.")
        return

    with open(NOTES_FILE, "r") as f:
        notes = f.readlines()

    if not notes:
        speak("You have no notes.")
        return

    speak("Here are your notes.")
    for note in notes:
        speak(note.strip())


def clear_notes():
    if os.path.exists(NOTES_FILE):
        open(NOTES_FILE, "w").close()
        speak("All notes have been cleared.")
    else:
        speak("There are no notes to clear.")


# COMMAND PROCESSOR

def process_command(command, state):
    command = command.lower().strip()

    if command == "":
        return True

    # Exit command
    if any(word in command for word in ["exit", "quit", "shutdown", "sleep"]):
        speak("Alright... shutting down. See you soon.")
        return False

    # Handle waiting sates
    if state[WAITING_FOR_CITY]:
        say_weather(command)
        state[WAITING_FOR_CITY] = False
        return True

    if state[WAITING_FOR_NOTE]:
        save_note(command)
        state[WAITING_FOR_NOTE] = False
        return True

    # Weather
    if "weather" in command:
        if "in" in command:
            city = command.split("in")[-1].strip()
            say_weather(city)
        else:
            speak("Please tell me the city name.")
            state[WAITING_FOR_CITY] = True
        return True

    # Notes
    if "take a note" in command or "write a note" in command:
        speak("What should I note?")
        state[WAITING_FOR_NOTE] = True
        return True

    if "read notes" in command:
        read_notes()
        return True

    if "clear notes" in command or "delete notes" in command:
        clear_notes()
        return True

    # Open websites
    if command.startswith("open "):
        site = command.replace("open ", "")
        webbrowser.open(f"https://{site}.com")
        return True

    # Play music
    if command.startswith("play"):
        song = command.replace("play", "").strip()
        link = musicLibrary.music.get(song)

        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I could not find that song")

        return True

    # Basic info
    if "your name" in command:
        speak("My name is Alexa")
        return True

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    if "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(today)
        return True

    if "day" in command:
        day = datetime.datetime.now().strftime("%A")
        speak(day)
        return True

    # News
    if "news" in command:
        say_news()
        return True

    # AI fallback
    try:
        reply = ask_ai(command)
        speak(reply)
    except Exception:
        speak("Sorry, I did not understand that command")

    return True


# MAIN PROGRAM

if __name__ == "__main__":
    speak("Initializing Alexa")

    running = True

    while running:
        try:
            # If waiting for user response (no wake word)
            if STATE[WAITING_FOR_CITY] or STATE[WAITING_FOR_NOTE]:
                command = listen()
                running = process_command(command, STATE)
                continue

            # Wake word listening
            wake_word = listen(timeout=3, phrase_time_limit=1).lower().strip()

            if wake_word == "alexa":
                speak("Yes")
                print("Alexa active...")

                command = listen()
                running = process_command(command, STATE)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except KeyboardInterrupt:
            speak("Goodbye")
            break
        except Exception as e:
            print("Error:", e)
