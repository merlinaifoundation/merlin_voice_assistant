from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self, greeter):
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
        self.fileRecording = None
        self.greeter = greeter
        self._canRecord = False
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
            if self._canRecord:
                # print("GreeterVoice Finished. Flushing...")

                self.initialize()
                self.startRecording(self.greeter.stopAction)
                self.stopRecording()

                userRecordedInputSize = 0
                
                if self.recorder:
                    userRecordedInput = self.recorder.HasRecordingObj()
                    userRecordedInputSize = len(userRecordedInput)

                    if userRecordedInputSize > 0:
                        print(
                            "Recording Size: ",
                            userRecordedInputSize,
                        )
                        if userRecordedInputSize > 17:
                            self.fileRecording = self.recorder.SaveRecordingObj()
                            self.recorder.CleanRecording()
                        else:
                            print("Discarding...")
                            self.reset()

            else:
                self.reset()

    def reset(self):
        timeNow = time.time()
        
        #if self.fileRecording is not None:
            #self.fileRecording = None
        
        if self.recorder and self.recorder.Finished():
            self._prGreen("Flushing Recording...", "Once")
            self.recorder.StopRecording()
            self.recorder.CleanRecording()
            self.recorder.RemoveRecording()
            self.recorder = None
            diff = round(time.time() - timeNow, 2)
            self._prRed("Reset Recorder in seconds: ", diff)

    def initialize(self):
        timeNow = time.time()
        if self.recorder is None:
            self.recorder = Recorder(None)
            diff = round(time.time() - timeNow, 2)
            self._prRed("Initialized Recorder in seconds: ", diff)

    def startRecording(self, stopAction):

        timeNow = time.time()
        if self.recorder and not self.recorder.Finished():
            print("Starting OpenMic...")
            self.recorder.StartRecording()
            self.listener.Listen(stopAction)
            self.listener.DetectSilence(stopAction)
            diff = round(time.time() - timeNow, 2)
            self._prRed("Listening for seconds: ", diff)
        #else:
            #self.Reset()

    def stopRecording(self):
        timeNow = time.time()
        if self.recorder and self.recorder.IsRecording():
            self.recorder.StopRecording()
            diff = round(time.time() - timeNow, 2)
            self._prRed("Stoping OpenMic for seconds: ", diff)

    def StartThread(self):
        self.start()
        
    def SetOpenMic(self, canRecord):
        self._canRecord = canRecord
