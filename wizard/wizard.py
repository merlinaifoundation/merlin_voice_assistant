from threading import Thread
import time

# import keyboard
# from decouple import config

from tapeRecorder.tape import TapeRecorder
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

        self.TapeRecorder = TapeRecorder()

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
        #sys.exit(None)

    def run(self):

        try:

            while not self._stop:

                time.sleep(0.001)

                enabled = self.Greeter.UserInvoked()
                cancelled = self.Greeter.UserCancelled()
                idle = self.Greeter.IsIdle()
                openMicOn = not cancelled and idle and enabled
                

                #status = int(enabled), int(cancelled), int(idle), int(openMicOn)
                #print("STATUS", status)
                self.TapeRecorder.SetOpenMic(openMicOn)
                # not finished the flags-implementation
                # bypass filter when cancelling!
                bypassFilter = cancelled
                self.TapeRecorder.SetBypassFilter(bypassFilter)
                self.TapeRecorder.SetCancelled(cancelled)

                # to start recording session
                self.TapeRecorder.FilterTape()
                filteredTape = self.TapeRecorder.GetFilteredTape()
                if filteredTape:
                    self.TapeRecorder.SaveTape(filteredTape)
                
                fileRecording = self.TapeRecorder.GetSavedTape()
                if fileRecording:
                    cancelled = self.Greeter.UserCancelled()
                    self.Brain.SetCancelled(cancelled)
                    self.Brain.SetQuery(fileRecording)

                cancelled = self.Greeter.UserCancelled()
                if not cancelled: 
                    idle = self.Greeter.IsIdle()
                    enabled = self.Greeter.UserInvoked()
                    if idle and enabled:
                        aiResponse = self.Brain.GetResponse()
                        if aiResponse:
                            self.Greeter.VoiceResponse(aiResponse)

                # if keyboard.is_pressed('q'):
                # raise Exception('Quitting...')

            self.Greeter.StopThread()
            self.Brain.StopThread()
            self.TapeRecorder.StopThread()

        except Exception as error:
            self._prRed("\nExiting Wizard Thread...", error)

        #sys.exit(None)
        
    def StartThread(self):

        timeNow = time.time()

        self.Greeter.StartThread()

        self.Brain.StartThread()

        self.TapeRecorder.StartThread()

        self.start()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("Wizard Thread Start in seconds: ", diff)
