from threading import Thread
import time

from libs.greeter import Greeter


class RunnerGreeter(Thread):

    def __init__(self):
        super().__init__()
        timeNow = time.time()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("Greeter Creation in seconds: ", diff)
        self.greeter =  Greeter()

    def _prRed(self, skk, number):
        print("\033[91m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number)

    def run(self):
        

        self.greeter.InitStopper()
        self.greeter.InitWaker()
        time.sleep(0.02)
        self.greeter.ForceWake()

        while True:

            time.sleep(0.01)

            self.greeter.CountIteration()
            #print("Doing nothing, Iter:", self.greeter.count)

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

                
            if self.greeter.wakeAction and self.greeter.wakeAction.IsInvoked():

                if not self.greeter.HasGreeted():
                    print("Welcome...")
                    self.greeter.voiceMaker.VoiceAwake()
                    self.greeter.SetHasGreeted(True)
                    time.sleep(1)
                    

