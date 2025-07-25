from gtts import gTTS
from playsound import playsound

# Create an instance of gTTS
tts = gTTS(text="Hello, this is a test.", lang='en')

# Save the speech to an mp3 file
tts.save("test.mp3")

# Play the saved audio file
playsound("test.mp3")
