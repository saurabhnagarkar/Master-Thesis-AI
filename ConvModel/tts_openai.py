from pathlib import Path
from openai import OpenAI
from playsound import playsound

# Initialize OpenAI client
client = OpenAI()

# Define the path for the speech file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create audio speech
def tts_openai(txt):
    response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",   
    input=txt
    )

    # Write the audio data to a file
    if response.content:
        with open(speech_file_path, 'wb') as f:
            f.write(response.content)
        print("Audio file created successfully.")

        # Play the audio file
        playsound(str(speech_file_path))
    else:
        print("No audio content received from API.")
