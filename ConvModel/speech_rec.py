import speech_recognition as sr
import os

def speech_rec():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            textsaid = recognizer.recognize_google(audio)
            print("You said:"+textsaid)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request result;{0}".format(e))
    return textsaid





