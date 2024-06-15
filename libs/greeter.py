from threading import Thread
import time
from decouple import config

from libs.actions import Action
from libs.textResponder import TextDisplay
from libs.voiceMaker import VoiceMaker

class Greeter(Thread):

    def __init__(self):
        super().__init__()
        timeNow = time.time()

        self.pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.stopWordFile = config("STOP_WORD_FILE")

        self.stopMode = 1
        self.wakeAction = None
        self.stopAction = None
        self._greeted = False
        self.count = 0
        
        self.voiceMaker = VoiceMaker()
        
        diff = round(time.time() - timeNow, 2)
        self._prGreen("Greeter Creation in seconds: ", diff)

    def _prRed(self,skk, number):
        print("\033[91m {}\033[00m".format(skk),number)

    def _prGreen(self,skk, number):
        print("\033[92m {}\033[00m".format(skk),number)
        
    def HasGreeted(self):
        return self._greeted

    def ResetWaker(self):
        self.wakeAction = None

    def ResetStopper(self):
        self.stopAction = None

    def InitWaker(self):
        timeNow = time.time()

        if self.wakeAction is None:
            self.wakeAction = Action(self.pv_access_key, self.wakeWordFile)
            self.wakeAction.StartListening()
        
        diff = round(time.time() - timeNow, 2)
        self._prRed("Init Waker in seconds: ", diff)

    def ForceWake(self):

        if self.wakeAction:
            self.wakeAction.SetInvoked(True)

    def InitStopper(self):
        timeNow = time.time()

        if self.stopAction is None:
            self.stopAction = Action(self.pv_access_key, self.stopWordFile)
            self.stopAction.StartListening()
            
        diff = round(time.time() - timeNow, 2)
        self._prRed("Init Stopper in seconds: ", diff)

    def UseDisplay(self, text):
        txtDisplay = TextDisplay()
        txtDisplay.Display(text)

    def SetHasGreeted(self, state):
        self._greeted = state

    def CountIteration(self):
        if self.count > 1000000:
            self.count = 0
        self.count += 1

    def UserCancelled(self):
        if self.stopAction and self.stopAction.IsInvoked():
            return True
        return False
