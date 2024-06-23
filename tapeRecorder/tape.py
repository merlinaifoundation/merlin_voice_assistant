from threading import Thread
import time
from decouple import config


class Filterer(Thread):

    def __init__(self):
        super().__init__()
        self.name = "Filter"

        timeNow = time.time()
        self._bypassFilter = False
        self._cancelled = False
        self._cummulativeFilteredBuffers = []
        self._userRecordedInput = None
        self._stopThread = False

        diff = round(time.time() - timeNow, 2)
        self._prGreen("\nTape Recorder Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[95m {}\033[00m".format(skk), number, end="", flush=True)

    def _prGreen(self, skk, number):
        print("\033[96m {}\033[00m".format(skk), number, end="", flush=True)

    def run(self):

        while not self._stopThread:

            time.sleep(0.001)

            try:

                if self._userRecordedInput:
                    userRecordedInputSize = len(self._userRecordedInput)
                    if userRecordedInputSize > 0:
                        self._prGreen(
                            "\nRecording Size: ",
                            userRecordedInputSize,
                        )
                        if userRecordedInputSize > 60 or self._bypassFilter:
                            self._cummulativeFilteredBuffers.append(
                                self._userRecordedInput
                            )

                            self._prGreen(
                                "\nPassed the filter: ", userRecordedInputSize
                            )
                        else:
                            self._prGreen(
                                "\nDiscarding short Recording: ", userRecordedInputSize
                            )
                            # self.Recorder.StopRecording(True)
                    self._userRecordedInput = None

                    # pass
            except Exception as error:
                self._prRed("\nError on Tape:", error)

        self.StopThread()
        # sys.exit(None)

    def FilterBuffer(self, userRecordedInput):
        self._userRecordedInput = userRecordedInput

    def StartThread(self):
        self.start()

    def StopThread(self):
        self.SetCancelled(True)
        self._stopThread = True

    def PickFilteredBuffer(self):
        if len(self._cummulativeFilteredBuffers) > 0:
            return self._cummulativeFilteredBuffers.pop(0)
        return None

    def SetCancelled(self, status):
        self._cancelled = status

    def SetBypassFilter(self, status):
        self._bypassFilter = status
