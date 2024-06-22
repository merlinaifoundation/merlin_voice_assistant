from threading import Thread
import time

# import keyboard
# from decouple import config

from tapeRecorder.tape import TapeRecorder
from ai.gpt import ChatGPT
from libs.greeter import Greeter
from tapeRecorder.openMic import OpenMic


class Wizard(Thread):

    def __init__(self):
        super().__init__()

        timeNow = time.time()
        self._prRed("Wizard Start-up...", None)

        # self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        # self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self.Greeter = Greeter()

        self.TapeRecorder = TapeRecorder()
        self.OpenMic = OpenMic()

        self.Brain = ChatGPT()

        self._stop = False
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Wizard Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[91m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number)

    def StopThread(self):
        self._stop = True
        # sys.exit(None)

    def run(self):

        try:

            while not self._stop:

                time.sleep(0.001)

                enabled = self.Greeter.UserInvoked()
                cancelled = self.Greeter.UserCancelled()
                idle = self.Greeter.IsIdle()
                openMicOn = not cancelled and idle and enabled
                # status = int(enabled), int(cancelled), int(idle), int(openMicOn)
                # print("STATUS", status)

                self.OpenMic.SetCancelled(cancelled or not idle)
                self.OpenMic.SetOpenMic(openMicOn)

                time.sleep(0.001)
                # to start recording session

                rawBuffer = self.OpenMic.TakeBuffer()

                cancelled = self.Greeter.UserCancelled()
                bypassFilter = cancelled
                self.TapeRecorder.SetBypassFilter(bypassFilter)
                self.TapeRecorder.SetCancelled(cancelled)
                self.TapeRecorder.FilterTapeBuffer(rawBuffer)

                time.sleep(0.001)

                filteredTapeBuffer = self.TapeRecorder.TakeFilteredBuffer()

                time.sleep(0.001)

                fileRecording = self.OpenMic.SaveBufferFile(filteredTapeBuffer)
                self.TapeRecorder.SaveTapeURL(fileRecording)

                time.sleep(0.001)

                tapeFile = self.TapeRecorder.TakeSavedTapeFile()

                cancelled = self.Greeter.UserCancelled()
                self.Brain.SetCancelled(cancelled)
                self.Brain.SetQuery(tapeFile)

                time.sleep(0.001)

                aiResponse = self.Brain.TakeResponse()

                if aiResponse:
                    time.sleep(0.001)

                    cancelled = self.Greeter.UserCancelled()
                    if cancelled:
                        self.Greeter.VoiceMaker.CreateWakeVoice(aiResponse, True)
                    else:
                        self.Greeter.VoiceResponse(aiResponse)

                time.sleep(0.001)

        except Exception as error:
            self._prRed("\nExiting Wizard Thread...", error)

        self.Greeter.StopThread()
        self.Brain.StopThread()
        self.OpenMic.StopThread()
        self.TapeRecorder.StopThread()

        # sys.exit(None)

    def StartThread(self):

        timeNow = time.time()

        self.Greeter.StartThread()
        self.Brain.StartThread()
        self.TapeRecorder.StartThread()
        self.OpenMic.StartThread()
        self.start()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("Wizard Thread Start in seconds: ", diff)
