from threading import Thread
import time
from decouple import config


class TapeRecorder(Thread):

    def __init__(self):
        super().__init__()

        timeNow = time.time()

        # self.Recorder = None
        self._bypassFilter = False
        self._cancelled = False
      
        self._cummulativeFilteredBuffers = []
        self._userRecordedInput = None

        self._stopThread = False
        self._initialize()
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Tape Recorder Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[94m {}\033[00m".format(skk), number)

    def run(self):

        while not self._stopThread:

            time.sleep(0.001)

            try:

                if self._userRecordedInput:
                    userRecordedInputSize = len(self._userRecordedInput)
                    if userRecordedInputSize > 0:
                        print(
                            "Recording Size: ",
                            userRecordedInputSize,
                        )
                        if userRecordedInputSize > 60 or self._bypassFilter:
                            self._cummulativeFilteredBuffers.append(self._userRecordedInput)
                            
                            self._prGreen("Passed the filter: ", userRecordedInputSize)
                        else:
                            self._prGreen("Discarding short Recording: ", userRecordedInputSize)
                            #self.Recorder.StopRecording(True)
                    self._userRecordedInput = None
                
                    #pass
            except Exception as error:
                self._prRed("\nError on Tape:", error)
       
        self.StopThread()
        # sys.exit(None)

    def FilterBuffer(self, userRecordedInput):
        self._userRecordedInput = userRecordedInput
        



    def _initialize(self):
        timeNow = time.time()
        diff = round(time.time() - timeNow, 2)
        self._prRed("Initialized Recorder in seconds: ", diff)

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
