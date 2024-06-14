from threading import Thread
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self):
        super().__init__()
        self.recorder = None

        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))
        print("Listener Settings")
        print(self._listenThreshold, self._silenceDuration, self._silenceThreshold)
        self.listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )

    def Reset(self):
        if self.recorder is not None:
            if self.recorder.IsRecording():
                print("Stopping Recording...")
                self.recorder.StopRecording()
            self.recorder.CleanRecording()
            self.recorder.RemoveRecording()
            self.recorder = None

    def Initialize(self):
        if self.recorder is None:
            self.recorder = Recorder(None)

    def Start(self, stopAction):

        if self.recorder and not self.recorder.Finished():
            print("Starting OpenMic...")
            self.recorder.StartRecording()
            self.listener.Listen(stopAction)
            self.listener.DetectSilence(stopAction)

    def Stop(self):
        if self.recorder and self.recorder.IsRecording():
            print("Stopping OpenMic...")
            self.recorder.StopRecording()
