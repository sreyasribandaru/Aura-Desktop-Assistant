import time
import threading
import pyttsx3
import queue

reminders = []

# Initialize TTS engine and queue
engine = pyttsx3.init()
speech_queue = queue.Queue()

def speak_worker():
    while True:
        text = speech_queue.get()
        if text == "QUIT":
            break
        print(f"Reminder: {text}")
        try:
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            print("Speech engine runtime error")
        speech_queue.task_done()

# Start the speech thread
speech_thread = threading.Thread(target=speak_worker, daemon=True)
speech_thread.start()

def speak(text):
    speech_queue.put(text)

def add_reminder(reminder_text, delay_seconds):
    reminder_time = time.time() + delay_seconds
    reminders.append((reminder_text, reminder_time))

    # Start background thread to wait and notify
    threading.Thread(target=wait_for_reminder, args=(reminder_text, reminder_time), daemon=True).start()
    return f"Reminder set for {delay_seconds} seconds from now."

def wait_for_reminder(reminder_text, reminder_time):
    while time.time() < reminder_time:
        time.sleep(1)
    speak(f"Reminder: {reminder_text}")

def check_reminders():
    if not reminders:
        return "No reminders set."
    return "\n".join([f"Reminder: {r[0]}" for r in reminders])

def get_upcoming_reminders(max_count=3):
    current_time = time.time()
    upcoming = [(text, time_) for text, time_ in reminders if time_ > current_time]
    upcoming.sort(key=lambda x: x[1])

    if not upcoming:
        return "No upcoming reminders."

    result = []
    for i, (text, time_) in enumerate(upcoming[:max_count]):
        time_left = time_ - current_time
        minutes, seconds = divmod(int(time_left), 60)
        hours, minutes = divmod(minutes, 60)

        time_str = ""
        if hours > 0:
            time_str += f"{hours}h "
        if minutes > 0:
            time_str += f"{minutes}m "
        time_str += f"{seconds}s"

        result.append(f"{i + 1}. '{text}' in {time_str}")

    return "\n".join(result)

def clear_reminders():
    reminders.clear()
    return "All reminders have been cleared."

# Optional cleanup when shutting down
def stop_speech_thread():
    speech_queue.put("QUIT")
    speech_thread.join()
