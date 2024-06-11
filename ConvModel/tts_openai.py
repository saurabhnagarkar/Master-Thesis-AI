from pathlib import Path
from openai import OpenAI
from playsound import playsound

# Initialize OpenAI client
client = OpenAI()

# Define the path for the speech file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create audio speech
def tts_openai(txt, output_filepath):
    response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",   
    input=txt
    )

    # Write the audio data to a file
    if response.content:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to file '{output_filepath}'")
        

        # Play the audio file
        playsound(str(speech_file_path))
    else:
        print("No audio content received from API.")
