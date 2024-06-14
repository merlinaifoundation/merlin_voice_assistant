from threading import Thread
from decouple import config

from hearer.listener import Listener
from hearer.recorder import Recorder


class Hearer(Thread):

    def __init__(self):
        super().__init__()
        self.recorder = None

        self.listener = Listener(0.45, 2.4, 0.4)

    def ResetRecorder(self):
        if self.recorder is not None:
            if self.recorder.IsRecording():
                print("Stopping Recording...")
                self.recorder.StopRecording()
            self.recorder.CleanRecording()
            self.recorder = None

    def InitRecorder(self):
        if self.recorder is None:
            self.recorder = Recorder(None)
