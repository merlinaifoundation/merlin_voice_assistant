from threading import Thread
import time

# from decouple import config

from tapeRecorder.base import TapeRecorder
from ai.gpt import ChatGPT
from libs.greeter import Greeter


class Wizard(Thread):

    def __init__(self):
        super().__init__()

        timeNow = time.time()
        self._prRed("Wizard Start-up...", None)

        # self._listenThreshold = float(config("LISTEN_THRESHOLD"))
        # self._silenceDuration = float(config("LISTEN_SILENCE_DURATION"))
        self.Greeter = Greeter()
        self.TapeRecorder = TapeRecorder(self.Greeter)
        self.Brain = ChatGPT()

        self._cancelled = False
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Wizard Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[97m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[98m {}\033[00m".format(skk), number)

    def run(self):

        try:

            

            while True:

                time.sleep(0.01)

                enabled = self.Greeter.UserInvoked()
                cancelled = self.Greeter.UserCancelled()
                idle = self.Greeter.IsIdle()
                openMicOn = idle and enabled

                status = int(enabled), int(cancelled), int(idle), int(openMicOn)
                # print("\nSTATUS", status)

                # bypass filter when cancelling!
                bypassFilter = cancelled
                self.TapeRecorder.SetBypassFilter(bypassFilter)

                # not finished the flags-implementation
                self.TapeRecorder.SetCancelled(cancelled)

                # to start recording session
                self.TapeRecorder.SetOpenMic(openMicOn)

                cancelled = self.Greeter.UserCancelled()

                self.Brain.MakeSummary(cancelled)

                # has record to process for answers?
                # brain.SetResponse(None)
                fileRecording = self.TapeRecorder.GetTape()

                self.Brain.SetQuery(fileRecording)
                # tapeRecorder.SetTape(None)
                self.TapeRecorder.SetTape(None)

                aiResponse = self.Brain.GetResponse()
                self.Greeter.VoiceResponse(aiResponse)

                if self.Greeter.IsIdle():
                    if aiResponse:
                        self.Brain.SetResponse(None)
                        self.TapeRecorder.resetTape()

        except Exception as error:
            print("\nExiting...", error)

    def StartThread(self):
        
        self.start()
        self.Brain.StartThread()
        self.TapeRecorder.StartThread()
        self.Greeter.StartThread()
        
        
