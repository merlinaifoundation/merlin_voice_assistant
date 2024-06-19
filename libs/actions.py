import os
from threading import Thread
import struct
import time
import pvporcupine
import pyaudio


class Action(Thread):

    def __init__(self, pv_access_key, wakeWordFile, channels , frame_length, rate):
        super().__init__()
        self._wake_pa = pyaudio.PyAudio()
        default_input_device = self._wake_pa.get_default_input_device_info()
        print(f"Default Input Device: {default_input_device['name']}")
        
        self._stop = True
        self._invoked = False
        self.wakeWordFile = wakeWordFile
        rootPath = os.path.dirname(__file__)
        self._keyword_path = os.path.join(rootPath, self.wakeWordFile)
        self._apiKey = str(pv_access_key)
        self._createClient( channels, frame_length, rate)
        self._openStream()

    def _createClient(self,  channels,  frame_length, rate):
        self.porcupineClient = pvporcupine.create(
            access_key=self._apiKey, keyword_paths=[self._keyword_path]
        )
        self._channels = channels or 1
        self.frame_length = frame_length  or self.porcupineClient.frame_length
        self.rate = rate or self.porcupineClient.sample_rate
        print("Actions params at: ", (self._channels, self.frame_length, self.rate)) #  (1, 512, 16000) or defaults
        
        

    def _openStream(self):
        
        self.porcupineStream = self._wake_pa.open(
            rate=self.rate ,
            channels=self._channels , # does not work stereo
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.frame_length
            
        )
        print("\nWakeWord Routine from: ", self.wakeWordFile)

    def StartListening(self):

        if not self._invoked:
            self._stop = False
            self.start()

    def IsInvoked(self):
        return self._invoked

    def SetInvoked(self, finalized):
        self._invoked = finalized
        if finalized:
            self._stop = True

    def run(self):

        try:

            while not self._stop:
                time.sleep(0.001)
                frameLength = self.frame_length or self.porcupineClient.frame_length
                porcupine_pcm = self.porcupineStream.read(frameLength)
                porcupine_pcm = struct.unpack_from("h" * frameLength, porcupine_pcm)
                porcupine_keyword_index = self.porcupineClient.process(porcupine_pcm)

                if porcupine_keyword_index >= 0:

                    self.SetInvoked(True)
                    print("\nAction Phrase Detected as in file: ", self.wakeWordFile)

        except Exception as error:
            print("Error Opening Wake Stream", error,  self.wakeWordFile)

        try:
        
            self.porcupineStream.stop_stream()
            self.porcupineStream.close()
            
        except Exception as error:
            print("Error Closing Wake Stream", error, self.wakeWordFile)
        
        try:
        
            self.porcupineClient.delete()
            self._wake_pa.terminate()
            
        except Exception as error:
            print("Error Terminating Wake Clients", error, self.wakeWordFile)
        