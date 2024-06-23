from threading import Thread
import time
from decouple import config

from tapeRecorder.listener import Listener
from tapeRecorder.recorder import Recorder


class OpenMic(Thread):

    def __init__(self):
        super().__init__()
        self.name = "OpenMic"

        timeNow = time.time()

        self._isOpenMic = False
        self._cancelled = False
        self._cummulativeTapeFiles = []
        self._stopThread = False

        self._initializeListener()
        self._initializeRecorder()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("\nOpenMic Creation in seconds: ", diff)

    def _initializeListener(self):
        timeNow = time.time()
        self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self._silenceThreshold = float(config("LISTEN_SILENCE_THRESHOLD"))
        self._prGreen(
            "\nListener Settings",
            (self._listenThreshold, self._silenceDuration, self._silenceThreshold),
        )
        self.Listener = Listener(
            self._listenThreshold, self._silenceDuration, self._silenceThreshold
        )
        diff = round(time.time() - timeNow, 2)
        self._prGreen("\nOpenMic Creation in seconds: ", diff)

    def _initializeRecorder(self):
        timeNow = time.time()
        self.Recorder = Recorder(None)
        diff = round(time.time() - timeNow, 2)
        self._prRed("\nInitialized Recorder in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number, end="", flush=True)

    def _prGreen(self, skk, number):
        print("\033[93m {}\033[00m".format(skk), number, end="", flush=True)

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
                    #this line kills comprehension I believe
                    #self.Recorder.StopRecording(True)
                    pass
            
            except Exception as error:
                self._prRed("\nError on Tape:", error)

        self.Recorder.StopRecording(True)
        self.Recorder.StopThread()
        # sys.exit(None)

    def StartThread(self):
        self.start()
        self.Recorder.StartThread()

    def StopThread(self):
        self._stopThread = True
        self.SetCancelled(True)

    def SetOpenMic(self, isOpenMic):
        self._isOpenMic = isOpenMic

    def PickBuffer(self):
        return self.Recorder.TakeRecordingBuffer()

    def SetCancelled(self, status):

        self.Listener.SetCancelled(self._cancelled)
        self._cancelled = status

    def SaveBufferToFile(self, inputBuffer):
        fileRecording = self.Recorder.SaveRecordingFile(inputBuffer)
        if fileRecording:
            self._cummulativeTapeFiles.append(fileRecording)
        # return fileRecording

    def DeleteBufferFile(self, file):
        return self.Recorder.DeleteRecordingFile(file)

    def PickBufferFilePath(self):
        if len(self._cummulativeTapeFiles) > 0:
            return self._cummulativeTapeFiles.pop(0)
        return None
