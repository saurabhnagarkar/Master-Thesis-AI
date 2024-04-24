from gpt_turbo import ChatApp
from speech_rec import speech_rec
from google_tts import google_tts


app = ChatApp(model="gpt-4") # the model that i am using


def main():
   while True:
       txt = speech_rec()
       res = app.chat(txt)
       google_tts(res)
       print(f"NPC : {res}")
if __name__ == "__main__":
   main()

    