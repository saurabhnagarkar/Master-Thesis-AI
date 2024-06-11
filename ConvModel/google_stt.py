import os
from google.cloud import speech
import pyaudio
import queue
import os
from datetime import datetime
import time
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/saurabhnagarkar/Master-Thesis-AI/ConvModel/inlaid-reactor-418023-bcce207793e3.json'


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            data = self._buff.get()
            if data is None:
                return
            data = [data]
            yield b''.join(data)

def listen_print_loop(responses):
    full_transcript = ""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            full_transcript += transcript + " "

    return full_transcript

def transcribe_file(speech_file):
    """Transcribes the given audio file."""
    client = speech.SpeechClient()
    
    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US'
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""

    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript


""" def main():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True  # Set this to False if you only want final results
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        # Return the final transcript
        return listen_print_loop(responses) """

def main():
    audio_file = '/Users/saurabhnagarkar/Master-Thesis-AI/AudioFiles/player_input.wav'
    return transcribe_file(audio_file)


if __name__ == '__main__':
    main()
