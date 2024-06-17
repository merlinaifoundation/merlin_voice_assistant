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

        self._pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.stopWordFile = config("STOP_WORD_FILE")

        self._stopMode = 1
        self.wakeAction = None
        self.stopAction = None
        self.iteration = 0

        self._greeted = False
        self._aiResponse = None

        self.voiceMaker = VoiceMaker()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("Greeter Creation in seconds: ", diff)

    def _prRed(self, skk, obj):
        print("\033[91m {}\033[00m".format(skk), obj)

    def _prGreen(self, skk, obj):
        print("\033[92m {}\033[00m".format(skk), obj)

    def _reset(self):

        print("Flushing...")
        self.resetWaker()
        # mode sleeping
        if self._stopMode == 1:
            print("Sleeping...")
            self.voiceMaker.VoiceSleeping()
        # mode interruption when greeter is talking
        if self._stopMode == 2:
            print("Processing User Interruption...")
            self.voiceMaker.VoiceProcess()

        # tapeRecorder.Reset()
        print("Restarting...")
        self.resetStopper()

        self.initWaker()
        # mode sleeping
        if self._stopMode == 1:
            self.setHasGreeted(False)
        # mode interruption when greeter is talking
        if self._stopMode == 2:
            self.forceWake()

        self.initStopper()

    def _awakening(self):

        if not self.hasGreeted():
            print("Welcome...")
            self.voiceMaker.VoiceAwake()
            self.setHasGreeted(True)
            # time.sleep(1)
            # return

        if self.voiceMaker.IsIdle():
            # print("GreeterVoice Finished. Flushing...")
            self._stopMode = 1

    def run(self):

        self.initStopper()
        self.initWaker()
        time.sleep(0.02)
        self.forceWake()

        while True:

            time.sleep(0.01)
            self.countIteration()
            # print("Doing nothing, Iter:", self.greeter.count)

            # checks if user asked to Stop
            if self.UserCancelled():
                self._reset()
                time.sleep(0.01)
                # continue

            if self.UserInvoked():
                self._awakening()

    def resetWaker(self):
        self.wakeAction = None

    def resetStopper(self):
        self.stopAction = None

    def initWaker(self):
        timeNow = time.time()

        if self.wakeAction is None:
            self.wakeAction = Action(self._pv_access_key, self.wakeWordFile)
            self.wakeAction.StartListening()

            diff = round(time.time() - timeNow, 2)
            self._prRed("Init Waker in seconds: ", diff)

    def initStopper(self):
        timeNow = time.time()
        if self.stopAction is None:
            self.stopAction = Action(self._pv_access_key, self.stopWordFile)
            self.stopAction.StartListening()
            diff = round(time.time() - timeNow, 2)
            self._prRed("Init Stopper in seconds: ", diff)

    def forceWake(self):
        if self.wakeAction:
            self.wakeAction.SetInvoked(True)

    def setHasGreeted(self, state):
        self._greeted = state

    def hasGreeted(self):
        return self._greeted

    def countIteration(self):
        if self.iteration > 1000000:
            self.iteration = 0
        self.iteration += 1

    #####################################################################################################

    def UseDisplay(self, text):
        txtDisplay = TextDisplay()
        txtDisplay.Display(text)

    def IsIdle(self):

        if self.voiceMaker.IsIdle() and self.hasGreeted():
            return True
        return False

    def UserCancelled(self):
        if self.stopAction and self.stopAction.IsInvoked():
            return True
        return False

    def UserInvoked(self):
        if self.wakeAction and self.wakeAction.IsInvoked():
            return True
        return False

    def StartThread(self):
        self.start()

    def VoiceResponse(self, response):

        self._aiResponse = response

        if self._aiResponse is not None:
            cancelled = self.UserCancelled()
            isIdle = self.IsIdle()
            enabled = self.UserInvoked()

            if isIdle:
                if enabled and not cancelled:
                    if len(self._aiResponse) > 300:
                        self.voiceMaker.VoiceWait()
                    self._prGreen("Display Response: ", self._aiResponse)
                    self._stopMode = 2
                    self.voiceMaker.VoiceDefault(self._aiResponse, cancelled)
                    # greeter.UseDisplay(aiResponse)
            if cancelled:
                self.voiceMaker.CreateWakeVoice(self._aiResponse, True)

        self._aiResponse = None
