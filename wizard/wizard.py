from threading import Thread
import time

# import keyboard
# from decouple import config

from tapeRecorder.tape import Filterer
from ai.gpt import ChatGPT
from libs.greeter import Greeter
from tapeRecorder.openMic import OpenMic


class Wizard(Thread):

    def __init__(self):
        super().__init__()

        self.name = "Wizard"
        timeNow = time.time()
        self._prRed("Wizard Start-up...", None)

        # self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        # self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self.Greeter = Greeter()

        self.Filter = Filterer()
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

                #activated?
                enabled = self.Greeter.UserInvoked()
                #cancelled?
                cancelled = self.Greeter.UserCancelled()
                #voice idle?
                idle = self.Greeter.IsIdle()
                openMicOn =  idle and enabled and not cancelled
                # status = int(enabled), int(cancelled), int(idle), int(openMicOn)
                # print("STATUS", status)
                self.OpenMic.SetCancelled(cancelled or not idle)
                self.OpenMic.SetOpenMic(openMicOn)

                time.sleep(0.001)
                # to start recording session
                
                cancelled = self.Greeter.UserCancelled()
                
                rawBuffer = self.OpenMic.PickBuffer()
                self.Filter.SetBypassFilter(cancelled)
                self.Filter.SetCancelled(cancelled)
                self.Filter.FilterBuffer(rawBuffer)
                time.sleep(0.001)
                filteredTapeBuffer = self.Filter.PickFilteredBuffer()
                self.OpenMic.SaveBufferToFile(filteredTapeBuffer)
                time.sleep(0.001)

                cancelled = self.Greeter.UserCancelled()
                tapeFilePath = self.OpenMic.PickBufferFilePath()
                self.Brain.SetCancelled(cancelled)
                self.Brain.SetQuery(tapeFilePath)
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
        self.Filter.StopThread()

        # sys.exit(None)

    def StartThread(self):

        timeNow = time.time()

        self.Greeter.StartThread()
        self.Brain.StartThread()
        self.Filter.StartThread()
        self.OpenMic.StartThread()
        self.start()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("Wizard Thread Start in seconds: ", diff)
