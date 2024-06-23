import os
import time
import pygame
from threading import Thread

# from gtts import gTTS
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from decouple import config
import random
from openai import OpenAI


class TextToSpeech(Thread):
    def __init__(self, language=None):
        super().__init__()
        self.name = 'Text to Speech'

        self._chat = None
        self._stop = True
        self._rootPath = os.path.dirname(__file__)
        self._fileName = str(random.randint(0, 1000000)) + ".mp3"
        self._setFilePath()
        self.mixer = pygame.mixer

        self._forceStopObj = None
        self._autoremoveFile = False
        self._mustPrepareFile = False
        self._mustPlayFile = False
        self._isBusy = False
        self.language = language or str(config("OUTPUT_SPEECH_LANG"))
        self._ttsModel = str(config('TTS_MODEL'))
        self._ttsVoiceModel =config('TTS_VOICE_MODEL')
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

        
        try:
            self._setFilePath()
            # defVoice  : Literal['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
            with self.client.audio.speech.with_streaming_response.create(
                model=self._ttsModel, 
                voice= 'alloy', #self._ttsVoiceModel , 
                input=str(self._chat)
            ) as tts_response:
                tts_response.stream_to_file(self._output_file)

        except Exception as error:
            print("\nError Preparing File TTS:", error)

    def _play(self):
        
        try:
            
            if not self._isBusy: 
                self._isBusy = True
                self._setFilePath()
                self.mixer.init()
                self.mixer.music.stop()
                self.mixer.music.load(self._output_file)
                if self._silentMode == 0:
                    self.mixer.music.play()
                    while self.mixer.music.get_busy() and not self._cancelled:
                        time.sleep(0.01)
                else:
                    # is in Silent Mode
                    time.sleep(0.2)

        except Exception as error:
            print("\nError Playing File TTS:", error)

        
        
    def _stopPlay(self):
        try:
            # self.mixer.music.stop()
            if self._isBusy: 
                self.mixer.music.stop()
                self.mixer.stop()
                #self.mixer.quit()
                #pass
        except Exception as error:
            print("\nError When Stoping TTS:", error)
            
        self._isBusy = False
        self._stop = True
        # self._chat = None

    def RemoveFile(self, file):
        try:
            if file is not None:
                self._fileName = file
            self._setFilePath()
            if os.path.isfile(self._output_file):
                os.remove(self._output_file)
                print("\nRemoving Voice File TTS: ", self._output_file)

        except Exception as error:
            print("\nError Voice File TTS:", error)

    def _runRoutine(self):
    
        if self._mustPrepareFile:
            self._prepareFile()
        if self._mustPlayFile:
            self._play()
            self._stopPlay()
            if self._autoremoveFile:
                self.RemoveFile(self._fileName)
    ####################################################################################################
    def run(self):
        
        self._runRoutine()
        
    def SetCancelled(self, cancelled):
        self._cancelled = cancelled

    # sets the fails and fails if it does not exist (for record play)
    def SetFile(self, file):
        self._fileName = file
        self._setFilePath()
        return os.path.isfile(self._output_file)

    def PrepareFileFromText(self, chat, asThread = False):

        self._chat = chat
        self._mustPrepareFile = True
        self._mustPlayFile = False
        if asThread:
            self.start()
        else:
            self._runRoutine()

    def SpeakFromText(self, chat, asThread = True):
        if (self._stop) and (chat is not None):
            self._stop = False
            self._chat = chat
            self._mustPrepareFile = True
            self._mustPlayFile = True
            self._autoremoveFile = True
            if asThread:
                self.start()
            else:
                self._runRoutine()
            

    def SpeakFromFile(self, file, asThread = False):
        if (self._stop) and (file is not None):
            self._stop = False
            if file is not None:
                self._fileName = file
            # some content to mark Finished(), in this case the filename as default
            self._mustPrepareFile = False
            self._mustPlayFile = True
            self._chat = self._fileName
            if asThread:
                self.start()
            else:
                self._runRoutine()

    def Finished(self):
        if not self._isBusy:
            return True
        #print("VOICE IS BUSY")
        return False
