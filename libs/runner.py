from threading import Thread
import time

from libs.greeter import Greeter


class RunnerGreeter(Thread):

    def __init__(self):
        super().__init__()
        timeNow = time.time()

        self._aiResponse = None
        self.greeter = Greeter()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("RunnerGreeter Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[91m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number)

    def SetContent(self,content):
        self._aiResponse = content
        
    def run(self):

        self.greeter.InitStopper()
        self.greeter.InitWaker()
        time.sleep(0.02)
        self.greeter.ForceWake()

        while True:

            time.sleep(0.01)

            self.greeter.CountIteration()
            # print("Doing nothing, Iter:", self.greeter.count)

            # checks if user asked to Stop
            if self.greeter.UserCancelled():

                print("Flushing...")
                self.greeter.ResetWaker()

                # mode sleeping
                if self.greeter.stopMode == 1:
                    print("Sleeping...")
                    self.greeter.voiceMaker.VoiceSleeping()

                # mode interruption when greeter is talking
                if self.greeter.stopMode == 2:
                    print("Processing Interruption...")
                    self.greeter.voiceMaker.VoiceProcess()

                # tapeRecorder.Reset()

                print("Restarting...")

                self.greeter.InitWaker()

                # mode sleeping
                if self.greeter.stopMode == 1:
                    self.greeter.SetHasGreeted(False)

                # mode interruption when greeter is talking
                if self.greeter.stopMode == 2:
                    self.greeter.ForceWake()

                self.greeter.ResetStopper()
                self.greeter.InitStopper()

                time.sleep(0.01)

                continue

            if self.greeter.UserInvoked():

                if not self.greeter.HasGreeted():
                    print("Welcome...")
                    self.greeter.voiceMaker.VoiceAwake()
                    self.greeter.SetHasGreeted(True)
                    time.sleep(1)

                if self.greeter.voiceMaker.IsIdle():
                    #self._aiResponse = None
                    #print("GreeterVoice Finished. Flushing...")
                    self.greeter.stopMode = 1

                if self._aiResponse is not None:

                    if len(self._aiResponse) > 300:
                        self.greeter.voiceMaker.VoiceWait()

                    print("Display Response: ", self._aiResponse)
                    self.greeter.stopMode = 2
                    self.greeter.voiceMaker.VoiceDefault(
                        self._aiResponse, self.greeter.stopAction
                    )
                    self._aiResponse = None
                    # greeter.UseDisplay(aiResponse)
