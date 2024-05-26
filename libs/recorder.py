from threading import Thread
from pvrecorder import PvRecorder
from decouple import config

class Recorder(Thread):
    def __init__(self, bufferLimit = None):
        super().__init__()
        self._buffer = []
        self._result = []
        self._is_recording = False
        self._stop = True
    
        cfgLimit = config("REC_BUFFER_LIMIT")
        self._bufferLimit = bufferLimit or int(cfgLimit) or 1e6
        print("Recording Buffer Limit set at: ", self._bufferLimit)
        self._finalized = False
        self.recorder = PvRecorder(device_index=-1, frame_length=512)

    def run(self):
        #start recording
        self.recorder.start()
        print("Recording...")
        while not self._stop:
            #read
            reading = self.recorder.read()
            #if more data than limit, clean buffer
            if (len(self._buffer) > self._bufferLimit):
                print('Recorder Buffer Limit was Hit', len(self._buffer), ". Flushing...")
                self._buffer = []
            #append to buffer
            if (len(reading)>0):
                self._buffer.extend(reading)
        #stop recording
        self.recorder.stop()
        #append result to final variable
        self._result = self._buffer.copy()
        
        #flags
        self._stop = True
        self._is_recording = False
        self._finalized = True

    def StartRecording(self):
        if self._stop and self._finalized is False :
            self._stop = False
            self._is_recording = True
            self.start()
 
    def IsRecording(self):
        return self._is_recording
    def Finished(self):
        return self._finalized
    def HasRecording(self):
        return self._result
    def CleanRecording(self):
        self._result = []
        self._buffer = []
    def StopRecording(self):
        self._stop = True
        while self._is_recording:
            pass
