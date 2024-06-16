from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self, greeter):
        super().__init__()

        timeNow = time.time()

        self._recorder = None
        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))
        self._cutLength = int(config("LISTEN_LENGTH"))

        print("Listener Settings")
        print(self._listenThreshold, self._silenceDuration, self._silenceThreshold)
        self._listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )
        self.fileRecording = None
        self.greeter = greeter
        self.isOpenMic = False
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
            if self.isOpenMic:
                # print("GreeterVoice Finished. Flushing...")

                self.initialize()
                self.startTape(self.greeter.stopAction)
                self.stopTape()
                
                self.filterTape()

            else:
                self.resetTape()



    def filterTape(self):
        userRecordedInputSize = 0
        if self._recorder:
            userRecordedInput = self._recorder.GetRecordingObj()
            userRecordedInputSize = len(userRecordedInput)
            if userRecordedInputSize > 0:
                print(
                    "Recording Size: ",
                    userRecordedInputSize,
                )
                if userRecordedInputSize > 93:
                    self.fileRecording = self._recorder.SaveRecordingObj()
                    self._recorder.CleanRecording()
                else:
                    print("Discarding short Recording:", userRecordedInputSize)
                    self.resetTape()
        
    def resetTape(self):
        timeNow = time.time()
        
        #if self.fileRecording is not None:
            #self.fileRecording = None
        
        if self._recorder and self._recorder.Finished():
            self._prGreen("Flushing Recording...", "Once")
            self._recorder.StopRecording()
            self._recorder.CleanRecording()
            self._recorder.RemoveRecording()
            self._recorder = None
            diff = round(time.time() - timeNow, 2)
            self._prRed("Reset Recorder in seconds: ", diff)

    def initialize(self):
        timeNow = time.time()
        if self._recorder is None:
            self._recorder = Recorder(None)
            diff = round(time.time() - timeNow, 2)
            self._prRed("Initialized Recorder in seconds: ", diff)

    def startTape(self, stopAction):

        timeNow = time.time()
        if self._recorder and not self._recorder.Finished():
            print("Starting OpenMic...")
            self._recorder.StartRecording()
            self._listener.Listen(stopAction)
            
            #DETECT WHEN VOICE ACTIVATES AND STORE RECORDING FROM THERE - BIAS (cut length)
            stored = self._recorder.GetBufferObj()
            getIndex = len(stored)
            print("Cutting at index =", getIndex)
            stored = stored[getIndex-self._cutLength:getIndex]
            self._recorder.SetBufferObj(stored)
            
            self._listener.DetectSilence(stopAction)
            diff = round(time.time() - timeNow, 2)
            self._prRed("Listening for seconds: ", diff)
        #else:
            #self.Reset()

    def stopTape(self):
        timeNow = time.time()
        if self._recorder and self._recorder.IsRecording():
            self._recorder.StopRecording()
            diff = round(time.time() - timeNow, 2)
            self._prRed("Stoping OpenMic for seconds: ", diff)

    def StartThread(self):
        self.start()
        
    def SetOpenMic(self, isOpenMic):
        self.isOpenMic = isOpenMic
