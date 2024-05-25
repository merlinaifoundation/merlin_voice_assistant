from threading import Thread
from decouple import config

from libs.actions import Action
from libs.textToSpeech import TextToSpeech
from libs.textResponder import TextDisplay
from libs.interpreter import Interpreter

class Greeter(Thread):

    def __init__(self):
        super().__init__()

        self.sleepingVoice = config("SLEEPING_VOICE")
        self.awakeVoice = config("AWAKE_VOICE")
        self.pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.stopWordFile = config("STOP_WORD_FILE")
        self.interpreter = Interpreter()
        self.wakeAction = None
        self.stopAction = None
        self.voice = None
        self._greeted = False

    def SpeechToText(self,userRecordedInput):
        transcript  = self.interpreter.SpeechToText(userRecordedInput)
        return transcript
    def SpeechToTextOpenAI(self,userRecordedInput):
        transcript  = self.interpreter.SpeechToTextOpenAI(userRecordedInput)
        return transcript
    def SleepingVoice(self):
        sleepVoiceObj = TextToSpeech()
        sleepVoiceObj.Tell(self.sleepingVoice)

    def HasGreeted(self):
        return self._greeted

    def ResetActions(self):
        self.wakeAction = None
        self.stopAction = None

    def ResetVoice(self):
        self.voice = None

    def IsIdle(self):
        return (self.voice is not None) and self.voice.Finished()

    def UseVoice(self, content):
        if self.voice is None:
            self.voice = TextToSpeech()
            self.voice.Tell(content)

    def InitActions(self):
        if self.wakeAction is None:
            self.wakeAction = Action(self.pv_access_key, self.wakeWordFile)
            self.wakeAction.Start()

        if self.stopAction is None:
            self.stopAction = Action(self.pv_access_key, self.stopWordFile)
            self.stopAction.Start()

    def AwakeVoice(self):
        awakeVoiceObj = TextToSpeech()
        awakeVoiceObj.Tell(self.awakeVoice)

    def UseDisplay(self, text):
        txtDisplay = TextDisplay()
        txtDisplay.Tell(text)

    def SetHasGreeted(self, state):
        self._greeted = state
