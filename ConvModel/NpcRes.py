from flask import Flask, request, jsonify
#from speech_rec import speech_rec
#from google_stt import transcribe_audio_file
from google_stt import main
from gpt_turbo import ChatApp
from google_tts import google_tts
from tts_openai import tts_openai
import os
import time
import csv
from datetime import datetime

app = Flask(__name__)
shared_folder_path = '/Users/saurabhnagarkar/Master-Thesis-AI/AudioFiles'
appname = ChatApp(model="gpt-4o", load_file='/Users/saurabhnagarkar/Master-Thesis-AI/ConvModel/context.json')

#function to calculate the latency for the processing time
def log_time(taken_time):
    filename = 'response_times.csv'
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as file:
        headers = ['Date and Time', 'Time Taken']
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(headers)  # Write header only if file does not exist
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([current_time, taken_time])

@app.route('/process_audio', methods=['POST'])
def process_audio():
    #audio_file = request.form['filename']
    #file_path = os.path.join(shared_folder_path, audio_file)
    start_time = time.time()

    #method for transcribing the audio using python on device library
    #txt = speech_rec() 
    #method to transcribe the audio file stored in the shared folder
    #txt = transcribe_audio_file() 

    # this script is tresponsible for recording as well as transcribing the audio into text with the google cloud API 
    txt = main()
    
    #res variable stores the generated text fetched from the GPT's API
    res = appname.chat(txt)
    
    #now we join the path for the output file to the shared folder path
    output_filepath = os.path.join(shared_folder_path, "response_output.mp3")  

    #google_tts method is called to convert the text into speech from google cloud API
    result_path = google_tts(res, output_filepath)

    #tts_openai method is called to convert the text into speech from openai Text to speech API
    #result_path = tts_openai(res, output_filepath)
    total_time = time.time() - start_time
    log_time(total_time)
    return jsonify({"response": "File processed successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


