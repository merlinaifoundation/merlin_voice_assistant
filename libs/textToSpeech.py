import os
import pygame
from threading import Thread

# from gtts import gTTS
from time import sleep
from os import environ
from pip._vendor.rich import status

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from decouple import config
import random
from openai import OpenAI


class TextToSpeech(Thread):
    def __init__(self, language=None):
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
        self._silentMode = int(config("SILENT_MODE")) or 0
        self.client = OpenAI(api_key=str(apiKey))
        self._cancelled = False


    def _setFilePath(self):
        self._output_file = os.path.join(
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
                tts_response.stream_to_file(self._output_file)

        except Exception as error:
            print("Error Preparing File TTS:", error)

    def _play(self):

        self._setFilePath()

        try:
            self.mixer.init()
            if self._silentMode == 0:
                self.mixer.music.load(self._output_file)
                self.mixer.music.play()
                while self.mixer.music.get_busy():
                    if self._cancelled:
                        break
                    sleep(0.02)
            else:
                sleep(0.01)

        except Exception as error:
            print("Error Playing File TTS:", error)

    def _stopPlay(self):
        try:
            #self.mixer.music.stop()
            self.mixer.quit()
        except Exception as error:
            print("Error When Stoping TTS:", error)
        self._stop = True
        # self._chat = None

    def RemoveFile(self, file):
        try:
            if file is not None:
                self._fileName = file
            self._setFilePath()
            if os.path.isfile(self._output_file):
                os.remove(self._output_file)
                print("Removing Voice File TTS: ", self._output_file)

        except Exception as error:
            print("Error Voice File TTS:", error)

    def PlayFile(self):

        self._play()
        self._stopPlay()
        if self._autoremoveFile:
            self.RemoveFile(self._fileName)

    def run(self):

        if self._shouldPrepareFile:
            self._prepareFile()
        self.PlayFile()

    ####################################################################################################

    def SetCancelled(self, cancelled):
        self._cancelled = cancelled

    # sets the fails and fails if it does not exist (for record play)
    def SetFile(self, file):
        self._fileName = file
        self._setFilePath()
        return os.path.isfile(self._output_file)

    def PrepareFileFromText(self, chat, asThread=False):

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
                self.PlayFile()

    def SpeakFromFile(self, file, asThread=False):
        if (self._stop) and (file is not None):
            self._stop = False
            if file is not None:
                self._fileName = file

            # some content to mark Finished(), in this case the filename as default
            self._chat = self._fileName
            if asThread:
                self.start()
            else:
                self.PlayFile()

    def Finished(self):
        return (self._stop) and (self._chat is not None)
