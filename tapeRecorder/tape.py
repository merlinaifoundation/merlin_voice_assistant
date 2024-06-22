from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class TapeRecorder(Thread):

    def __init__(self):
        super().__init__()

        timeNow = time.time()

        # self.Recorder = None
        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))

        print("Listener Settings")
        print(self._listenThreshold, self._silenceDuration, self._silenceThreshold)
        self.Listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )
        self._isOpenMic = False
        self._bypassFilter = False
        self._cancelled = False
        self._cummulative = []
        self._cummulativeFiltered = []

        self._stop = False
        self._initialize()
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Tape Recorder Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def run(self):

        while not self._stop:

            time.sleep(0.001)

            try:

                if self._isOpenMic:

                    time.sleep(0.001)
                    timeNow = time.time()
                    
                    if not self.Recorder.IsRecording():
                        self.Recorder.StartRecording()
                    #
                    if self.Recorder.IsRecording():

                        self._prRed("\nStarting OpenMic...", timeNow)
                        self.Listener.Listen()
                        ###################################################
                        
                        self.Recorder.TrimLeftRecording()
                        
                        self.Listener.DetectSilence()
                        ###################################################
                        
                        self.Recorder.StopRecording()
                        diff = round(time.time() - timeNow, 2)
                        self._prRed("OpenMic Listening for seconds: ", diff)

            except Exception as error:
                self._prRed("Error on Tape:", error)

        self.Recorder.StopRecording(True)
        self.Recorder.StopThread()
        # sys.exit(None)

    def FilterTape(self):
        userRecordedInput = self.Recorder.GetRecordingObj()
        userRecordedInputSize = len(userRecordedInput)
        if userRecordedInputSize > 0:
            print(
                "Recording Size: ",
                userRecordedInputSize,
            )
            if userRecordedInputSize > 60 or self._bypassFilter:
                self._cummulativeFiltered.append(userRecordedInput)
                self._prGreen("Passed the filter: ", userRecordedInputSize)
            else:
                self._prGreen("Discarding short Recording: ", userRecordedInputSize)
                self.Recorder.StopRecording(True)

    def SaveTape(self, obj):
        if obj:
            fileRecording = self.Recorder.SaveRecordingObj(obj)
            if fileRecording:
                self._cummulative.append(fileRecording)

    # def Reset(self):
    # timeNow = time.time()

    # if self.Recorder.Finished():
    # self._prGreen("Flushing Recording...", "Once")
    # self.Recorder.StopRecording()
    # self.Recorder.NotifyFiltered()
    # self.Recorder.RemoveRecording()
    # self.Recorder = None
    # diff = round(time.time() - timeNow, 2)
    # self._prRed("Reset Recorder in seconds: ", diff)

    def _initialize(self):
        timeNow = time.time()

        self.Recorder = Recorder(None)

        diff = round(time.time() - timeNow, 2)
        self._prRed("Initialized Recorder in seconds: ", diff)

    def StartThread(self):
        self.start()
        self.Recorder.StartThread()

    def StopThread(self):
        self._stop = True
        self.SetCancelled(True)

    def SetOpenMic(self, isOpenMic):
        self._isOpenMic = isOpenMic

    # def SetTape(self, obj):
    # self._fileRecording = obj
    def GetFilteredTape(self):
        if len(self._cummulativeFiltered) > 0:
            return self._cummulativeFiltered.pop(0)
        return None

    def GetSavedTape(self):
        if len(self._cummulative) > 0:
            return self._cummulative.pop(0)
        return None

    def SetCancelled(self, status):
        
        self.Listener.SetCancelled(self._cancelled)
        self._cancelled = status
        #

    def SetBypassFilter(self, status):
        self._bypassFilter = status
