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
        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 10000)) + ".mp3"
        self.output_file = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )
        self.mixer = pygame.mixer
        self.mixer.init()
        self.lang = str(config("OUTPUT_SPEECH_LANG"))

    def Stop(self):
        try:
            
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
            
            tts = gTTS(text=self.chat, lang=self.lang)
            # You can specify other languages by changing the 'lang' parameter
            tts.save(self.output_file)
            self.mixer.music.load(self.output_file)
            self.mixer.music.play()
            while self.mixer.music.get_busy():
                sleep(0.1)
            self.mixer.music.stop()

        except Exception as error:
            print("Error:", error)

        self.Stop()

    def Tell(self, chat):
        if (self._stop) and (chat is not None):
            self._stop = False
            self.chat = chat
            self.start()

    def Finished(self):
        return (self._stop) and (self.chat is not None)
