import os
import pygame
from threading import Thread
#from gtts import gTTS
from time import sleep
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from decouple import config
import random
from openai import OpenAI

class TextToSpeech(Thread):
    def __init__(self):
        super().__init__()
        self.chat = None
        self._stop = True
        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self.output_file = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )
        self.mixer = pygame.mixer
        self.mixer.init()
        self.lang = str(config("OUTPUT_SPEECH_LANG"))
        OPENAI_API_KEY = config("OPENAI_API_KEY")

        self.client = OpenAI(api_key=str(OPENAI_API_KEY))
    def Stop(self):
        try:
            self.mixer.music.stop()
            self.mixer.quit()

        except Exception as error:
            print("Error:", error)

        try:
            os.remove(self.output_file)

        except Exception as error:
            print("Error:", error)

        
        self._stop = True
    
    def run(self):

        try:
           
            # You can specify other languages by changing the 'lang' parameter

            #tts = gTTS(text=self.chat, lang=self.lang)
            #tts.save(self.output_file)

            with self.client.audio.speech.with_streaming_response.create(model="tts-1", voice="alloy", input=str(self.chat)) as tts_response:
                tts_response.stream_to_file(self.output_file)
            
            self.mixer.music.load(self.output_file)
            self.mixer.music.play()
            while self.mixer.music.get_busy():
                sleep(0.1)
            

        except Exception as error:
            print("Error:", error)

        self.Stop()

    def SpeakFromText(self, chat):
        if (self._stop) and (chat is not None):
            self._stop = False
            self.chat = chat
            self.start()

    def Finished(self):
        return (self._stop) and (self.chat is not None)
