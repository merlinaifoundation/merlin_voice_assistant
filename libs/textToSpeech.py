import os
import pygame
from threading import Thread

# from gtts import gTTS
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
        self._rootPath = os.path.dirname(__file__)
        self._fileName = str(random.randint(0, 1000000)) + ".mp3"
        self._autoremove = False
        self._setFilePath()
        self.mixer = pygame.mixer
        self._forceStopObj = None

        self.lang = str(config("OUTPUT_SPEECH_LANG"))
        OPENAI_API_KEY = config("OPENAI_API_KEY")

        self.client = OpenAI(api_key=str(OPENAI_API_KEY))

    def SetForceStopObj(self, obj):
        self._forceStopObj = obj

    def _stopProcess(self):
        try:
            self.mixer.music.stop()
            self.mixer.quit()

        except Exception as error:
            print("Error:", error)

        self._stop = True

    def _removeFile(self, file):
        try:
            if file is not None:
                self._fileName = file
            self._setFilePath()
            os.remove(self.output_file)
        except Exception as error:
            print("Error Removing File:", error)

    def _setFilePath(self):
        self.output_file = os.path.join(
            self._rootPath,
            "defaultVoices",
            self._fileName,
        )

    def _prepareFile(self):

        self._setFilePath()
        try:

            # You can specify other languages by changing the 'lang' parameter
            # tts = gTTS(text=self.chat, lang=self.lang)
            # tts.save(self.output_file)
            with self.client.audio.speech.with_streaming_response.create(
                model="tts-1", voice="alloy", input=str(self.chat)
            ) as tts_response:
                tts_response.stream_to_file(self.output_file)

        except Exception as error:
            print("Error Preparing File:", error)

    def _playFile(self):

        self._setFilePath()

        try:
            self.mixer.init()
            self.mixer.music.load(self.output_file)
            self.mixer.music.play()
            while self.mixer.music.get_busy():
                sleep(0.5)
                if self._forceStopObj and self._forceStopObj.IsInvoked():
                    break

        except Exception as error:
            print("Error Playing File:", error)

    def _startProcess(self):

        self._playFile()
        self._stopProcess()
        if self._autoremove:
            self._removeFile(self._fileName)

    def SetFile(self, file):
        self._fileName = file
        self._setFilePath()
        return os.path.isfile(self.output_file)

    def PrepareFileFromText(self, chat):

        self.chat = chat
        self._prepareFile()

    def SpeakFromText(self, chat):
        if (self._stop) and (chat is not None):
            self._stop = False
            self.chat = chat
            self.PrepareFileFromText(self.chat)
            self._autoremove = True
            self._startProcess()

    def SpeakFromFile(self, file):
        if (self._stop) and (file is not None):
            self._stop = False
            if file is not None:
                self._fileName = file
            self._startProcess()

    def Finished(self):
        return (self._stop) and (self.chat is not None)
