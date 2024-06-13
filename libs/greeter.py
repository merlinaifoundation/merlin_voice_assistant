from threading import Thread
from decouple import config

from libs.actions import Action
from libs.textToSpeech import TextToSpeech
from libs.textResponder import TextDisplay


class Greeter(Thread):

    def __init__(self):
        super().__init__()

        self.sleepingVoiceTxt = config("SLEEPING_VOICE")
        self.awakeVoiceTxt = config("AWAKE_VOICE")
        self.pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.waitVoiceTxt = config("WAIT_VOICE")
        self.initVoiceTxt = config("INIT_VOICE")
        self.processVoiceTxt = config("PROCESSING_VOICE")

        self.stopWordFile = config("STOP_WORD_FILE")

        self._sleepingInnerFile = "StopVoice.mp3"
        self._awakeInnerFile = "WakeVoice.mp3"
        self._waitInnerFile = "WaitVoice.mp3"
        self._initInnerFile = "InitVoice.mp3"
        self._processInnerFile = "ProcessVoice.mp3"

        self._prepareInitialVoice()
        self._prepareDefaultVoices()

        self.wakeAction = None
        self.stopAction = None
        self._greeted = False
        self.firstTimeLoading = True
        self.count = 0

    def _prepareInitialVoice(self):

        self._initVoiceObj = TextToSpeech()
        if self._initVoiceObj.SetFile(self._initInnerFile) is False:
            self._initVoiceObj.PrepareFileFromText(self.initVoiceTxt)
        print("Initializing...")
        self.VoiceInit()

    def _prepareDefaultVoices(self):

        self._defaultVoiceObj = TextToSpeech()

        self._waitVoiceObj = TextToSpeech()
        if self._waitVoiceObj.SetFile(self._waitInnerFile) is False:
            self._waitVoiceObj.PrepareFileFromText(self.waitVoiceTxt)
            print("Creating Wait Audio File...")
        self.VoiceWait()

        self._processVoiceObj = TextToSpeech()
        if self._processVoiceObj.SetFile(self._processInnerFile) is False:
            self._processVoiceObj.PrepareFileFromText(self.processVoiceTxt)
            print("Creating Process Audio File...")

        self._sleepVoiceObj = TextToSpeech()
        if self._sleepVoiceObj.SetFile(self._sleepingInnerFile) is False:
            self._sleepVoiceObj.PrepareFileFromText(self.sleepingVoiceTxt)
            print("Creating Stop Audio File...")

        self._awakeVoiceObj = TextToSpeech()
        if self._awakeVoiceObj.SetFile(self._awakeInnerFile) is False:
            self._awakeVoiceObj.PrepareFileFromText(self.awakeVoiceTxt)
            print("Creating Wake Audio File...")

        print("Finished creating the TTS Defaults")

    def VoiceSleeping(self):
        self._sleepVoiceObj.SpeakFromFile(self._sleepingInnerFile)

    def VoiceAwake(self):
        self._awakeVoiceObj.SpeakFromFile(self._awakeInnerFile)

    def VoiceWait(self):
        self._waitVoiceObj.SpeakFromFile(self._waitInnerFile)

    def VoiceProcess(self):
        self._processVoiceObj.SpeakFromFile(self._processInnerFile)

    def VoiceInit(self):
        self._initVoiceObj.SpeakFromFile(self._initInnerFile)

    def VoiceDefault(self, content, stopObj):

        self._defaultVoiceObj.SetForceStopObj(stopObj)
        self._defaultVoiceObj.SpeakFromText(content)

    def HasGreeted(self):
        return self._greeted

    def ResetWaker(self):
        self.wakeAction = None

    def ResetStopper(self):
        self.stopAction = None

    def IsIdle(self):
        return (self._defaultVoiceObj is not None) and self._defaultVoiceObj.Finished()

    def InitWaker(self):
        if self.wakeAction is None:
            self.wakeAction = Action(self.pv_access_key, self.wakeWordFile)
            self.wakeAction.StartListening()

    def WakeOnFirstLoad(self):
        if self.firstTimeLoading:
            self.firstTimeLoading = False
            if self.wakeAction:
                self.wakeAction.SetInvoked(True)

    def InitStopper(self):
        if self.stopAction is None:
            self.stopAction = Action(self.pv_access_key, self.stopWordFile)
            self.stopAction.StartListening()

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
