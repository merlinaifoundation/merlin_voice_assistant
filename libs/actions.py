import os
import sys
from threading import Thread
import struct
import pvporcupine
import pyaudio


class Action(Thread):

    def __init__(self, pv_access_key , wakeWordFile ):
        super().__init__()
        self.wake_pa = pyaudio.PyAudio()
        self._stop = True
        self._invoked = False
        self.wakeWordFile = wakeWordFile
        rootPath = os.path.dirname(__file__)
        keyword_path = os.path.join(rootPath, self.wakeWordFile)

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

    def Start(self):
        
        if not self._invoked:
            self._stop = False
            self.start()

    def IsInvoked(self):
        return self._invoked
    
    def SetInvoked(self, finalized):
        self._invoked = finalized
        if (finalized):
            self._stop = True
  

    def run(self):

        try:

            print("\nWakeWord Routine from: ", self.wakeWordFile )

            devnull = os.open(os.devnull, os.O_WRONLY)
            old_stderr = os.dup(2)
            sys.stderr.flush()
            os.dup2(devnull, 2)
            os.close(devnull)

            while not self._stop:
                
                frameLength = self.porcupine.frame_length
                porcupine_pcm = self.porcupine_audio_stream.read(frameLength)
                porcupine_pcm = struct.unpack_from("h" * frameLength, porcupine_pcm)
                porcupine_keyword_index = self.porcupine.process(porcupine_pcm)

                if porcupine_keyword_index >= 0:
                    
                    self.porcupine_audio_stream.stop_stream()
                    self.porcupine_audio_stream.close()
                    self.porcupine.delete()
                    os.dup2(old_stderr, 2)
                    os.close(old_stderr)
                    
                    print("\nAction Phrase Detected as in file: ",  self.wakeWordFile)
                    self.SetInvoked(True)

        except Exception as error:
            print("Error:", error)
            
        
