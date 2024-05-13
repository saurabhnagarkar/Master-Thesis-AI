from google.cloud import texttospeech
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/saurabhnagarkar/Master-Thesis-AI/ConvModel/inlaid-reactor-418023-bcce207793e3.json'

client = texttospeech.TextToSpeechClient()
# Instantiates a client


# Set the text input to be synthesized
def google_tts(inputtxt, output_filepath):
    synthesis_input = texttospeech.SynthesisInput(text=inputtxt)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-D",
        #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file, overwriting the existing file each time
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filepath}'")

    # Play the output file
    return output_filepath