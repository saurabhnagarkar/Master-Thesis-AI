""" import speech_recognition as sr
import os
import time
from datetime import datetime

def speech_rec():
    recognizer = sr.Recognizer()

    with sr.AudioFile('/Users/saurabhnagarkar/Master-Thesis-AI/AudioFiles/player_input.wav') as source:
        audio = recognizer.record(source)

    try:
        textsaid = recognizer.recognize_google(audio)
        print("You said:"+textsaid)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request result;{0}".format(e))
    print(textsaid)
 """
import speech_recognition as sr
import time
from datetime import datetime

# Create a Recognizer instance
recognizer = sr.Recognizer()

# Capture audio input from the microphone
with sr.Microphone() as source:
 start_time = time.time()
 print("Speak something...")
 audio_data = recognizer.listen(source)

# Perform speech recognition using Google Web Speech API
try:
 text = recognizer.recognize_google(audio_data)
 print("You said:", text)
 print("Time taken:", time.time() - start_time)
except sr.UnknownValueError:
 print("Sorry, could not understand audio.")
except sr.RequestError as e:
 print("Error: Could not request results from Google Speech Recognition service;")



