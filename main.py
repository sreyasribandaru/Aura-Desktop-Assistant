import time
import threading
import pyttsx3
import datetime
import os
import webbrowser
from generate_email import generate_email
from reminder import add_reminder, check_reminders, clear_reminders, get_upcoming_reminders
from difflib import get_close_matches
import re
import speech_recognition as sr
import pygame
from gtts import gTTS
from serpapi import GoogleSearch
import requests


# Initialize speech engine
engine = pyttsx3.init()
# Get the available voices
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# Command templates with more flexibility in recognition
# Command templates with added language change functionality
commands = {
    "open youtube": "Open YouTube",
    "youtube": "Open YouTube",
    "open wikipedia": "Open Wikipedia",
    "wikipedia": "Open Wikipedia",
    "open google": "Open Google",
    "google": "Open Google",
    "what is your name": "What is your name",
    "who are you": "What is your name",
    "what can you do": "What can you do",
    "what is the meaning of your name": "Meaning of Aura",
    "meaning of your name": "Meaning of Aura",
    "what does your name mean": "Meaning of Aura",
    "help": "What can you do",
    "what time is it": "What is the time",
    "tell me the time": "What is the time",
    "time": "What is the time",
    "open spotify": "Open Spotify",
    "spotify": "Open Spotify",
    "play music": "Play music",
    "pause music": "Play music",
    "next song": "Next track",
    "skip song": "Next track",
    "previous song": "Previous track",
    "go back": "Previous track",
    "volume up": "Volume up",
    "increase volume": "Volume up",
    "volume down": "Volume down",
    "decrease volume": "Volume down",
    "generate email": "Generate email",
    "write email": "Generate email",
    "add reminder": "Add reminder",
    "remind me": "Add reminder",
    "set reminder": "Add reminder",
    "check reminders": "Check reminders",
    "list reminders": "Check reminders",
    "my reminders": "Check reminders",
    "upcoming reminders": "Get upcoming reminders",
    "next reminders": "Get upcoming reminders",
    "clear reminders": "Clear reminders",
    "delete reminders": "Clear reminders",
    "aura search": "Search Google",
    "search": "Search Google",
    "search something": "Search Google",
    "exit": "Exit",
    "quit": "Exit",
    "goodbye": "Exit",
    "change language": "Change language",  # New command for language change
    "set language": "Change language"  # Another possible variation

}

# Function to change the language
# Modify `process_command` to handle language change with separate listening

def say(text):
    """Use text-to-speech to say the given text"""
    print(f"{text}")
    engine.say(text)
    engine.runAndWait()

def listen(return_text=False, prompt=None):
    """Listen for voice commands using speech recognition"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if prompt:
                say(prompt)
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)

        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")

        if return_text:
            return command.lower()
        else:
            process_command(command.lower())

    except sr.WaitTimeoutError:
        if not return_text:
            say("No speech detected. I'm still listening.")
        return "" if return_text else None
    except sr.UnknownValueError:
        if not return_text:
            say("Sorry, I didn't understand that.")
        return "" if return_text else None
    except sr.RequestError:
        say("Speech recognition service is unavailable.")
        return "" if return_text else None
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        if not return_text:
            say("Sorry, there was an error with speech recognition.")
        return "" if return_text else None

def process_command(query):
    """Process the user's command"""
    query = query.lower().strip()

    # Check for 'and close' and process it
    and_close = False
    if " and close" in query:
        query = query.replace(" and close", "").strip()
        and_close = True

    # Try to find an exact match
    if query in commands:
        command = commands[query]
        if and_close:
            command += " and close"
        execute_command(command)
        return

    # Try to find a close match
    best_match = get_close_matches(query, commands.keys(), n=1, cutoff=0.6)
    if best_match:
        command = commands[best_match[0]]
        if and_close:
            command += " and close"
        execute_command(command)
        return

    # Fallback: check for keywords in query
    for key in commands:
        if key in query:
            command = commands[key]
            if and_close:
                command += " and close"
            execute_command(command)
            return

    say("Sorry, I couldn't understand that command.")

def play_pause_music():
    import pyautogui
    pyautogui.press('playpause')  # Simulates pressing the media play/pause key
def next_track():
    import pyautogui
    pyautogui.press('nexttrack')  # Simulates next media key

def previous_track():
    import pyautogui
    pyautogui.press('prevtrack')  # Simulates previous media key

def volume_up():
    import pyautogui
    pyautogui.press('volumeup')  # Increases system volume

def volume_down():
    import pyautogui
    pyautogui.press('volumedown')  # Decreases system volume
def search_google_serpapi(query):
    api_key = ""  # 🔁 Replace with your real API key
    url = "" #Replace url
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Try to extract the best available info
    if "answer_box" in data and "snippet" in data["answer_box"]:
        return data["answer_box"]["snippet"]
    elif "organic_results" in data and len(data["organic_results"]) > 0:
        return data["organic_results"][0]["snippet"]
    else:
        return "Sorry, I couldn't find any useful results."


def execute_command(command):
    """Execute the identified command"""
    global running  # Ensure 'running' flag is accessible

    # Check if the command contains 'and close', which will trigger the shutdown after the action
    if 'and close' in command:
        base_command = command.split("and close")[0].strip()

        if base_command == "Open YouTube":
            say("Opening YouTube and shutting down.")
            webbrowser.open("https://www.youtube.com")
            running = False  # Stop the assistant after opening
            return

        elif base_command == "Open Wikipedia":
            say("Opening Wikipedia and shutting down.")
            webbrowser.open("https://www.wikipedia.org")
            running = False  # Stop the assistant after opening
            return

        elif base_command == "Open Google":
            say("Opening Google and shutting down.")
            webbrowser.open("https://www.google.com")
            running = False  # Stop the assistant after opening
            return

        elif base_command == "Open Spotify":
            say("Opening Spotify and shutting down.")
            try:
                os.startfile("spotify")
            except FileNotFoundError:
                say("Spotify application not found. Make sure it is installed.")
            except Exception as e:
                say(f"An error occurred while trying to open Spotify: {e}")
            running = False  # Stop the assistant after opening
            return

    # Continue with normal commands (without 'and close')
    if command == "Open YouTube":
        say("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif command == "Open Wikipedia":
        say("Opening Wikipedia")
        webbrowser.open("https://www.wikipedia.org")

    elif command == "Open Google":
        say("Opening Google")
        webbrowser.open("https://www.google.com")

    elif command == "What is your name":
        say("I am Aura, your virtual desktop assistant.")

    elif command == "What can you do":
        say("I can open websites like YouTube, Wikipedia, and Google. I can generate emails, set reminders, tell the time, and play music. Just ask me what you need.")

    elif command == "What is the time":
        now = datetime.datetime.now()
        say(f"The current time is {now.strftime('%H:%M')}")

    elif command == "Open Spotify":
        say("Opening Spotify")
        try:
            os.startfile("spotify")
        except FileNotFoundError:
            say("Spotify application not found. Make sure it is installed.")
        except Exception as e:
            say(f"An error occurred while trying to open Spotify: {e}")

    elif command == "Generate email":
        say("What kind of email would you like me to generate?")
        prompt = listen(return_text=True)
        if prompt:
            say("Generating your email now...")
            generate_email(prompt)
            say("Email has been generated.")
        else:
            say("I didn't catch what kind of email you wanted to generate.")

    elif command == "Add reminder":
        try:
            reminder_text = listen(return_text=True, prompt="What should I remind you about?")
            if not reminder_text:
                say("I couldn't understand what to remind you about.")
                return

            delay_text = listen(return_text=True, prompt="In how many seconds, minutes, or hours?")
            if not delay_text:
                say("I couldn't understand the time for the reminder.")
                return

            # Try to extract a number from the response
            delay_seconds = extract_time_from_text(delay_text)

            if delay_seconds is None or delay_seconds <= 0:
                say("Sorry, I couldn't understand the time specified.")
                return

            response = add_reminder(reminder_text, delay_seconds)

            # Pause listening for the reminder time
            stop_listening_for_reminder(delay_seconds)

            say(response)
        except Exception as e:
            say(f"Sorry, I couldn't set the reminder. Error: {e}")

    elif command == "Check reminders":
        response = check_reminders()
        say(response)

    elif command == "Get upcoming reminders":
        response = get_upcoming_reminders()
        say(response)

    elif command == "Clear reminders":
        say("Are you sure you want to clear all reminders? Say yes or no.")
        confirmation = listen(return_text=True)
        if confirmation and "yes" in confirmation.lower():
            response = clear_reminders()
            say(response)
        else:
            say("Reminders were not cleared.")
    elif command == "Search Google":
        say("What should I search for?")
        query = listen(return_text=True)
        if query:
            say("Let me look that up for you...")
            try:
                result = search_google_serpapi(query)
                say(result)
            except Exception as e:
                say("Sorry, something went wrong while searching.")
                print("Search error:", e)
        else:
            say("I didn't catch the search query.")
    elif command == "Meaning of Aura":
        say("Aura means a unique energy, a radiant presence that surrounds and uplifts. I was named Aura because I'm here to bring lightness, clarity, and calm to your digital world — just like an aura reflects the essence of a soul.")

    elif command == "Exit":
        say("Goodbye! Aura is shutting down.")
        running = False

    elif command == "Play music":
        say("Toggling music playback.")
        play_pause_music()

    elif command == "Next track":
        say("Playing next track.")
        next_track()

    elif command == "Previous track":
        say("Going to previous track.")
        previous_track()

    elif command == "Volume up":
        say("Increasing volume.")
        volume_up()

    elif command == "Volume down":
        say("Decreasing volume.")
        volume_down()


def stop_listening_for_reminder(delay_seconds):
    """Pause listening for the given number of seconds"""
    print(f"Pausing listening for {delay_seconds} seconds.")
    time.sleep(delay_seconds)
    # After the delay, we can trigger the reminder and resume listening
    say("Reminder time has passed. I will now resume listening.")
    listen()  # Resume listening after the reminder time has passed

def extract_time_from_text(text):
    """Extract time in seconds from a text string"""
    # Example inputs: "5 seconds", "2 minutes", "1 hour", "two minutes", etc.

    # First check for digit numbers with regex
    seconds_match = re.search(r'(\d+)\s*(?:second|sec)s?', text)
    minutes_match = re.search(r'(\d+)\s*(?:minute|min)s?', text)
    hours_match = re.search(r'(\d+)\s*(?:hour|hr)s?', text)

    # Extract the first number if no unit is specified
    general_number = re.search(r'(\d+)', text)

    # Calculate seconds
    delay_seconds = 0

    if seconds_match:
        delay_seconds += int(seconds_match.group(1))
    if minutes_match:
        delay_seconds += int(minutes_match.group(1)) * 60
    if hours_match:
        delay_seconds += int(hours_match.group(1)) * 3600

    # If no specific time unit was found but we have a number
    if delay_seconds == 0 and general_number:
        # Assume seconds if just a number is given
        delay_seconds = int(general_number.group(1))

    return delay_seconds

# Main execution loop
if __name__ == "__main__":
    running = True
    say(f"{datetime.datetime.now().strftime('%H:%M')} - Aura is activated and ready to assist you.")

    while running:
        try:
            listen()
            time.sleep(0.5)  # Short pause to prevent high CPU usage
        except KeyboardInterrupt:
            say("Aura is shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            say("I encountered an error. Please try again.")
