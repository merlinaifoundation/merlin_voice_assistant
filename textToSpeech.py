import os
import pygame
from threading import Thread
from gtts import gTTS
from time import sleep
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from decouple import config
import random 

class TextToSpeech(Thread):
    def __init__(self):
        super().__init__()
        self.chat = None
        self._stop = True

        self.lang = str(config("OUTPUT_SPEECH_LANG"))
        self.output_file = str(random.randint(0,10000))

    def run(self):

        pygame.mixer.init()
        tts = gTTS(
            text=self.chat, lang=self.lang
        )  # You can specify other languages by changing the 'lang' parameter
        try:

            
            tts.save(self.output_file)

            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                sleep(0.2)
            
        except Exception as error:
            print("Error:", error)
        
        pygame.mixer.quit()
        os.remove(self.output_file)
        tts = None
        self._stop = True

    def Tell(self, chat):
        if (self._stop ) and (chat is not None):
            self._stop = False
            self.chat = chat
            self.start()

    def Finished(self):
        return (self._stop) and (self.chat is not None)
