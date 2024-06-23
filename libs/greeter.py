from threading import Thread
import time
from decouple import config

from libs.actions import Action
from libs.textResponder import TextDisplay
from libs.voiceMaker import VoiceMaker


class Greeter(Thread):

    def __init__(self):
        super().__init__()
        self.name = "Greeter"

        timeNow = time.time()

        self._pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.stopWordFile = config("STOP_WORD_FILE")

        self._actionVoiceFrameLength = int(config("WAKE_WORD_FRAME_LENGTH")) or None
        self._activationVoiceRate = int(config("WAKE_WORD_FRAME_RATE")) or None
        self._activationVoiceChannels = int(config("WAKE_WORD_CHANNELS")) or None

        self._greeted = False
        self._aiResponse = None
        self._stop = False
        self._stopMode = 1
        self.iteration = 0
        
        self.VoiceMaker = VoiceMaker()

        self.initWaker()
        self.initStopper()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("\nGreeter Creation in seconds: ", diff)

    def _prRed(self, skk, obj):
        print("\033[95m {}\033[00m".format(skk), obj, end='', flush=True)

    def _prGreen(self, skk, obj):
        print("\033[90m {}\033[00m".format(skk), obj, end='', flush=True)

    def _reset(self):

        print("\nFlushing Greeter...")
        self.WakeAction.StopListening()

        # mode sleeping
        if self._stopMode == 1:
            self._prRed("\nSleeping...", None)
            self.VoiceMaker.VoiceSleeping()
        # mode interruption when greeter is talking
        if self._stopMode == 2:
            self._prRed("\nProcessing User Interruption...", None)
            self.VoiceMaker.VoiceProcess()

        while self._aiResponse is None:
            self._prRed("\nWaiting for other processes...", None)
            time.sleep(0.05)

        self.VoiceMaker.CreateWakeVoice(self._aiResponse, True)
        self._aiResponse = None

        self.StopAction.StopListening()

        self.WakeAction.StartListening()
        # mode sleeping
        if self._stopMode == 1:
            self.setHasGreeted(False)
        # mode interruption when greeter is talking
        if self._stopMode == 2:
            self.forceWake()

        self.StopAction.StartListening()

        self._prGreen("\nWaiting for user...", None)

    def _awakening(self):

        if not self.hasGreeted():
            self._prGreen("\nWelcome...", None)
            self.VoiceMaker.VoiceAwake()
            self.setHasGreeted(True)
            # time.sleep(1)
            # return

        if self.VoiceMaker.IsIdle():
            # print("GreeterVoice Finished. Flushing...")
            self._stopMode = 1
        else:
            self._stopMode = 2

        if self._aiResponse is not None:
            if self.IsIdle():
                text = str(self._aiResponse)
                self._aiResponse = None
                if not self.UserCancelled():
                    if len(text) > 300:
                        self.VoiceMaker.VoiceWait()
                    self._prGreen("\nDisplay Response: ", text)
                    self.VoiceMaker.VoiceDefault(text)
                    # self.UseDisplay(aiResponse)

    def run(self):

        self.StopAction.StartListening()
        time.sleep(0.001)
        self.WakeAction.StartListening()
        time.sleep(0.001)
        self.forceWake()
        time.sleep(0.001)

        while not self._stop:

            time.sleep(0.001)
            self.countIteration()
            # print("Doing nothing, Iter:", self.greeter.count)
            cancelled = self.UserCancelled()
            self.VoiceMaker.SetCancelled(cancelled)
            # checks if user asked to Stop
            if cancelled:
                self._reset()

            if self.UserInvoked():
                self._awakening()


        # exit...
        self.StopAction.StopListening()
        self.WakeAction.StopListening()

    def initWaker(self):

        timeNow = time.time()

        self.WakeAction = Action(
            self._pv_access_key,
            self.wakeWordFile,
            self._activationVoiceChannels,
            self._actionVoiceFrameLength,
            self._activationVoiceRate,
        )
        self.WakeAction.StartThread()
        diff = round(time.time() - timeNow, 2)
        self._prRed("\nInit Waker in seconds: ", diff)

    def initStopper(self):
        timeNow = time.time()
        self.StopAction = Action(
            self._pv_access_key,
            self.stopWordFile,
            self._activationVoiceChannels,
            self._actionVoiceFrameLength,
            self._activationVoiceRate,
        )
        self.StopAction.StartThread()
        diff = round(time.time() - timeNow, 2)
        self._prRed("\nInit Stopper in seconds: ", diff)

    def forceWake(self):
        if self.WakeAction:
            self.WakeAction.SetInvoked(True)

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

        if self.VoiceMaker.IsIdle() and self.hasGreeted():
            return True
        return False

    def UserCancelled(self):
        if self.StopAction and self.StopAction.IsInvoked():
            return True
        return False

    def UserInvoked(self):
        if self.WakeAction and self.WakeAction.IsInvoked():
            return True
        return False

    def StartThread(self):
        self.start()

    def StopThread(self):
        self._stop = True

    def VoiceResponse(self, response):

        if response:
            self._aiResponse = response
