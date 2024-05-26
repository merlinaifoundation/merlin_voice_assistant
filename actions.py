import os
import sys
from time import sleep
from threading import Thread
import struct
from decouple import config
from colorama import Fore
import pvporcupine

import pyaudio

from textToSpeech import TextToSpeech


class Actions(Thread):

    def __init__(self, wordTag):
        super().__init__()
        self.wordTag = wordTag
        self.wake_pa = pyaudio.PyAudio()
        self._stop = True
        self._finalized = False
        self.porcupine = None
        self.porcupine_audio_stream =None
        pv_access_key = config("PV_ACCESS_KEY")
        wakeWordFile = config(wordTag)
      
        rootPath = os.path.dirname(__file__)
        keyword_path = os.path.join(rootPath, wakeWordFile)

        # print("Using WAKE WORD", keyword_path)

        self.porcupine = pvporcupine.create(
            access_key=pv_access_key, keyword_paths=[keyword_path]
        )

        self.porcupine_audio_stream = self.wake_pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

    def Enable(self):
        
        if not self._finalized:
            self._stop = False
            self.start()

    def IsEnabled(self):
        return self._finalized
        
    def SleepingVoice(self):
        voice2 = TextToSpeech()
        voice2.Tell("Ok, I'll stop!")
    def AwakeVoice(self):
        voice2 = TextToSpeech()
        voice2.Tell("I'm here!")
        

    def run(self):

        try:

            print(Fore.GREEN + "\nWakeWord Routine: ", self.wordTag)

            devnull = os.open(os.devnull, os.O_WRONLY)
            old_stderr = os.dup(2)
            sys.stderr.flush()
            os.dup2(devnull, 2)
            os.close(devnull)

            while self._stop != True:
                
                porcupine_pcm = self.porcupine_audio_stream.read(
                    self.porcupine.frame_length
                )
                porcupine_pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length, porcupine_pcm
                )

                porcupine_keyword_index = self.porcupine.process(porcupine_pcm)
                # print(Fore.GREEN + "\nWake word check\n", porcupine_keyword_index)

                if porcupine_keyword_index >= 0:
                    print(Fore.GREEN + "\nWake word detected\n")
                    self.porcupine_audio_stream.stop_stream()
                    self.porcupine_audio_stream.close()
                    self.porcupine.delete()
                    os.dup2(old_stderr, 2)
                    os.close(old_stderr)
                    self._stop = True

        except Exception as error:
            print("Error:", error)
            
        self._finalized = True
