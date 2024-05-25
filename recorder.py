from threading import Thread
from pvrecorder import PvRecorder


class Recorder(Thread):
    def __init__(self):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = True
        self._result = []
        self._finalized = False
        self.recorder = PvRecorder(device_index=-1, frame_length=512)

    def run(self):
        
        self.recorder.start()
        print("Recording...")
        while not self._stop:
            self._pcm.extend(self.recorder.read())
        self.recorder.stop()
        self._stop = True
        self._result = self._pcm.copy()
        
        self._is_recording = False
        self._finalized = True

    def StartRecording(self):
        if self._stop and self._finalized is False :
            self._stop = False
            self._is_recording = True
            self.start()
 
    def IsRecording(self):
        return self._is_recording
    def IsNew(self):
        return self._finalized is False
    def HasRecording(self):
        return self._result
    def CleanRecording(self):
        self._result = []
    def StopRecording(self):
        self._stop = True
        while self._is_recording:
            pass
