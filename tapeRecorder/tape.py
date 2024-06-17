from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self):
        super().__init__()

        timeNow = time.time()

        self.Recorder = None
        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))

        print("Listener Settings")
        print(self._listenThreshold, self._silenceDuration, self._silenceThreshold)
        self.Listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )
        self._fileRecording = None
        self._isOpenMic = False
        self._bypassFilter = False
        self._cancelled = False
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Tape Recorder Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def run(self):

        while True:

            time.sleep(0.01)
            
            # check if voice finished to start recording again
            if self._isOpenMic:
                # print("GreeterVoice Finished. Flushing...")

                self.initialize()
                self.startTape()
                self.stopTape()
                
                self.filterTape()

            else:
                self.Reset()



    def filterTape(self):
        userRecordedInputSize = 0
        if self.Recorder:
            userRecordedInput = self.Recorder.GetRecordingObj()
            userRecordedInputSize = len(userRecordedInput)
            if userRecordedInputSize > 0:
                print(
                    "Recording Size: ",
                    userRecordedInputSize,
                )
                if userRecordedInputSize > 93 or self._bypassFilter:
                    self._fileRecording = self.Recorder.SaveRecordingObj()
                    self.Recorder.CleanRecording()
                else:
                    print("Discarding short Recording:", userRecordedInputSize)
                    self.Reset()
        
    def Reset(self):
        timeNow = time.time()
        
        #if self.fileRecording is not None:
            #self.fileRecording = None
        
        if self.Recorder and self.Recorder.Finished():
            self._prGreen("Flushing Recording...", "Once")
            self.Recorder.StopRecording()
            self.Recorder.CleanRecording()
            self.Recorder.RemoveRecording()
            self.Recorder = None
            diff = round(time.time() - timeNow, 2)
            self._prRed("Reset Recorder in seconds: ", diff)

    
    def initialize(self):
        timeNow = time.time()
        if self.Recorder is None:
            self.Recorder = Recorder(None)
            diff = round(time.time() - timeNow, 2)
            self._prRed("Initialized Recorder in seconds: ", diff)
    
    def startTape(self):

        timeNow = time.time()
        
        if self.Recorder:
            
            if not self.Recorder.Finished():
                
                print("Starting OpenMic...")
                #
                self.Recorder.StartRecording()
                #
                self.Listener.Listen()
                #
                self.Recorder.TrimLeftRecording()
                #
                self.Listener.DetectSilence()
                #
                diff = round(time.time() - timeNow, 2)
                self._prRed("Listening for seconds: ", diff)
            #else:
                #self.Reset()

    def stopTape(self):
        timeNow = time.time()
        if self.Recorder and self.Recorder.IsRecording():
            self.Recorder.StopRecording()
            diff = round(time.time() - timeNow, 2)
            self._prRed("Stoping OpenMic for seconds: ", diff)

    def StartThread(self):
        self.start()
        
    def SetOpenMic(self, isOpenMic):
        self._isOpenMic = isOpenMic
    
    def SetTape(self, obj):
        self._fileRecording = obj
    def GetTape(self):
        return self._fileRecording
    
    def SetCancelled(self, status):
        self._cancelled = status
        self.Listener.SetCancelled(self._cancelled)
        #
        
    def SetBypassFilter(self, status):
        self._bypassFilter = status
    
