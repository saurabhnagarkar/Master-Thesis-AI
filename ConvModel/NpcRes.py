from flask import Flask, request, jsonify
from speech_rec import speech_rec
from gpt_turbo import ChatApp
from google_tts import google_tts
import os

app = Flask(__name__)
shared_folder_path = '/Users/saurabhnagarkar/Master-Thesis-AI/AudioFiles'
appname = ChatApp(model="gpt-3.5-turbo", load_file='/Users/saurabhnagarkar/Master-Thesis-AI/ConvModel/context.json')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    #audio_file = request.form['filename']
    #file_path = os.path.join(shared_folder_path, audio_file)
    txt = speech_rec()  
    res = appname.chat(txt)
    output_filepath = os.path.join(shared_folder_path, "response_output.mp3")  
    result_path = google_tts(res, output_filepath)
    return jsonify({"response": "File processed successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)




""" from gpt_turbo import ChatApp
from speech_rec import speech_rec
from google_tts import google_tts
import os


app = ChatApp(model="gpt-3.5-turbo", load_file='context.json') # the model that i am using




def main():
   while True:
       txt = speech_rec()
       res = app.chat(txt)
       google_tts(res)
       print(f"NPC : {res}")
if __name__ == "__main__":
   main()

     """


