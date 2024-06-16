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
    def __init__(self, language = None):
        super().__init__()
        self._chat = None
        self._stop = True
        self._rootPath = os.path.dirname(__file__)
        self._fileName = str(random.randint(0, 1000000)) + ".mp3"
        self._setFilePath()
        self.mixer = pygame.mixer
        self._forceStopObj = None
        self._autoremoveFile = False
        self._shouldPrepareFile = False
        self._shouldPlayFile = True
        self.language = language or str(config("OUTPUT_SPEECH_LANG"))

        apiKey = config("OPENAI_API_KEY")

        self.client = OpenAI(api_key=str(apiKey))

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
                model="tts-1", voice="alloy", input=str(self._chat)
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
                sleep(0.1)
                if self._forceStopObj and self._forceStopObj.IsInvoked():
                    break

        except Exception as error:
            print("Error Playing File:", error)

    def stop(self):
        try:
            self.mixer.music.stop()
            self.mixer.quit()
        except Exception as error:
            print("Error:", error)
        self._stop = True
        #self._chat = None

    def removeFile(self, file):
        try:
            if file is not None:
                self._fileName = file
            self._setFilePath()
            os.remove(self.output_file)
        except Exception as error:
            print("Error Removing File:", error)

    def playFile(self):

        self._playFile()
        self.stop()
        if self._autoremoveFile:
            self.removeFile(self._fileName)

    def run(self):

        if self._shouldPrepareFile:
            self._prepareFile()
        self.playFile()

    ####################################################################################################

    def SetForceStopObj(self, obj):
        self._forceStopObj = obj

    def SetFile(self, file):
        self._fileName = file
        self._setFilePath()
        return os.path.isfile(self.output_file)

    def PrepareFileFromText(self, chat, asThread = False):

        self._chat = chat
        if asThread:
            self._shouldPlayFile = False
            self.start()
        else:
            self._prepareFile()

    def SpeakFromText(self, chat, asThread=False):
        if (self._stop) and (chat is not None):
            self._stop = False
            self._chat = chat
            self._shouldPrepareFile = True
            self._autoremoveFile = True
            if asThread:
                self.start()
            else:
                self._prepareFile()
                self.playFile()

    def SpeakFromFile(self, file, asThread=False):
        if (self._stop) and (file is not None):
            self._stop = False
            if file is not None:
                self._fileName = file
            
            #some content to mark Finished(), in this case the filename as default
            self._chat = self._fileName 
            if asThread:
                self.start()
            else:
                self.playFile()

    def Finished(self):
        return (self._stop) and (self._chat is not None)
