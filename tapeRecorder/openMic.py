from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class OpenMic(Thread):

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
        self._cancelled = False

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
                        self._prRed("\nOpenMic Listening for seconds: ", diff)
                else:
                    self.Recorder.StopRecording(True)
                    #pass
            except Exception as error:
                self._prRed("\nError on Tape:", error)

        self.Recorder.StopRecording(True)
        self.Recorder.StopThread()
        # sys.exit(None)

    def _initialize(self):
        timeNow = time.time()
        self.Recorder = Recorder(None)
        diff = round(time.time() - timeNow, 2)
        self._prRed("Initialized Recorder in seconds: ", diff)

    def StartThread(self):
        self.start()
        self.Recorder.StartThread()

    def StopThread(self):
        self._stopThread = True
        self.SetCancelled(True)

    def SetOpenMic(self, isOpenMic):
        self._isOpenMic = isOpenMic

    def TakeBuffer(self):
        return self.Recorder.TakeRecordingBuffer()
        
    def SetCancelled(self, status):
        
        self.Listener.SetCancelled(self._cancelled)
        self._cancelled = status
        
    def SaveBufferFile(self, inputBuffer):
        return self.Recorder.SaveRecordingFile(inputBuffer)
    
    def DeleteBufferFile(self, file):
        return self.Recorder.DeleteRecordingFile(file)
