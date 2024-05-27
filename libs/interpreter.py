from threading import Thread
#from decouple import config
from time import sleep
from openai import OpenAI
import os


class InterpreterAI(Thread):

    def __init__(self):
        super().__init__()
        self.client = OpenAI()

       

    def SpeechToText(self, file ):

        transcription = ""
        
        try:
            audio_file = open(file, "rb")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        except Exception as e:
            print("Error", e)
        
        return transcription
