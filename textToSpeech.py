import os
import pygame
from threading import Thread
from gtts import gTTS
from time import sleep
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from decouple import config


class TextToSpeech(Thread):
    def __init__(self):
        super().__init__()
        self.chat = None
        self._stop = False

        self.lang = str(config("OUTPUT_SPEECH_LANG"))
        self.output_file = str(config("OUTPUT_SPEECH"))

    def Tell(self, chat):
        self.chat = chat
        self.start()

    def run(self):

        pygame.mixer.init()
        tts = gTTS(
            text=self.chat, lang=self.lang
        )  # You can specify other languages by changing the 'lang' parameter
        try:

            os.remove(self.output_file)
            tts.save(self.output_file)

            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                sleep(0.2)

        except Exception as error:
            print("Error:", error)

        pygame.mixer.quit()
        tts = None
        self._stop = True
        self.chat = None
