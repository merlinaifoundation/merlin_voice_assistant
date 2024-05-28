from threading import Thread
#from decouple import config
from time import sleep
from openai import OpenAI
from decouple import config

class InterpreterAI(Thread):

    def __init__(self):
        super().__init__()
        OPENAI_API_KEY = config("OPENAI_API_KEY")

        self.client = OpenAI(api_key= str(OPENAI_API_KEY))

       

    def SpeechToText(self, file, response_format):

        transcription = ""
        
        try:
            audio_file = open(file, "rb")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format=response_format
            )
        except Exception as e:
            print("Error", e)
        
        return transcription
