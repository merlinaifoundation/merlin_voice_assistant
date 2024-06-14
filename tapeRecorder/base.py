from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self):
        super().__init__()
        
        timeNow = time.time()
        
        self.recorder = None
        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))
        print("Listener Settings")
        print(self._listenThreshold, self._silenceDuration, self._silenceThreshold)
        self.listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )
        
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Tape Recorder Creation in seconds: ", diff)

    def _prRed(self,skk, number):
        print("\033[91m {}\033[00m".format(skk),number)

    def _prGreen(self,skk, number):
        print("\033[92m {}\033[00m".format(skk),number)


    def Reset(self):
        timeNow = time.time()
        if self.recorder is not None:
            if self.recorder.IsRecording():
                print("Stopping Recording...")
                self.recorder.StopRecording()
            self.recorder.CleanRecording()
            self.recorder.RemoveRecording()
            self.recorder = None
        diff = round(time.time() - timeNow, 2)
        self._prRed("Reset Recorder in seconds: ", diff)

    def Initialize(self):
        timeNow = time.time()
        if self.recorder is None:
            self.recorder = Recorder(None)
        diff = round(time.time() - timeNow, 2)
        self._prRed("Initialized Recorder in seconds: ", diff)

    def Start(self, stopAction):

        timeNow = time.time()
        if self.recorder and not self.recorder.Finished():
            print("Starting OpenMic...")
            self.recorder.StartRecording()
            self.listener.Listen(stopAction)
            self.listener.DetectSilence(stopAction)
        
        diff = round(time.time() - timeNow, 2)
        self._prRed("Listening for seconds: ", diff)

    def Stop(self):
        timeNow = time.time()
        if self.recorder and self.recorder.IsRecording():
            self.recorder.StopRecording()
        diff = round(time.time() - timeNow, 2)
        self._prRed("Stoping OpenMic for seconds: ", diff)
