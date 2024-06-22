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

                # check if voice finished to start recording again

                time.sleep(0.001)

                if self._isOpenMic:

                    self.Recorder.StartRecording()

                    #
                    if self.Recorder.IsRecording():

                        print("Starting OpenMic...")
                        #
                        timeNow = time.time()

                        self.Listener.Listen()
                        #
                        self.Recorder.TrimLeftRecording()
                        #
                        self.Listener.DetectSilence()

                        diff = round(time.time() - timeNow, 2)
                        self._prRed("Listening for seconds: ", diff)

                        self.Recorder.StopRecording()
                        diff = round(time.time() - timeNow, 2)
                        self._prRed("Stoping OpenMic for seconds: ", diff)

                else:
                    pass
                    # self.Recorder.StopRecording(True)

            except Exception as error:
                print("Error on Tape:", error)

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
            if userRecordedInputSize > 93 or self._bypassFilter:
                self._cummulativeFiltered.append(userRecordedInput)
                print("Passed the filter: ", userRecordedInputSize)
            else:
                print("Discarding short Recording: ", userRecordedInputSize)
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
        self._cancelled = status
        self.Listener.SetCancelled(self._cancelled)
        #

    def SetBypassFilter(self, status):
        self._bypassFilter = status
