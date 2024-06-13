from threading import Thread
from decouple import config

from libs.actions import Action
from libs.textToSpeech import TextToSpeech
from libs.textResponder import TextDisplay
from libs.interpreter import InterpreterAI

class Greeter(Thread):

    def __init__(self):
        super().__init__()

        self.sleepingVoiceTxt = config("SLEEPING_VOICE")
        self.awakeVoiceTxt = config("AWAKE_VOICE")
        self.pv_access_key = config("PV_ACCESS_KEY")
        self.wakeWordFile = config("WAKE_WORD_FILE")
        self.waitVoiceTxt = config("WAIT_VOICE")

        self.stopWordFile = config("STOP_WORD_FILE")
        
        self._stopInnerFile  = "StopVoice.mp3"
        self._wakeInnerFile  = "WakeVoice.mp3"
        self._waitInnerFile  = "WaitVoice.mp3"

        
        self._prepareInitialVoice()
        
        self.wakeAction = None
        self.stopAction = None
        self._voice = None
        self._greeted = False
        
        self.interpreter = InterpreterAI()
        
        self._prepareDefaultVoices()

    def SpeechToText(self,userRecordedInput):
        transcript  = self.interpreter.SpeechToText(userRecordedInput, "text")
        return transcript
    
    def _prepareInitialVoice(self):
        
        self._waitVoiceObj = TextToSpeech()
        self._waitVoiceObj.SetFile(self._waitInnerFile)
        self._waitVoiceObj.PrepareFileFromText(self.waitVoiceTxt)
        print("Initializing...")
        self.VoiceWait()
        
        
    def _prepareDefaultVoices(self):
        
        print("Creating Stop Audio File...")
        self._sleepVoiceObj = TextToSpeech()
        self._sleepVoiceObj.SetFile(self._stopInnerFile)
        self._sleepVoiceObj.PrepareFileFromText(self.sleepingVoiceTxt)
        print("Creating Wake Audio File...")
        self._awakeVoiceObj = TextToSpeech()
        self._awakeVoiceObj.SetFile(self._wakeInnerFile)
        self._awakeVoiceObj.PrepareFileFromText(self.awakeVoiceTxt)
        print("Finished creating the default voices")
    
        
    def VoiceSleeping(self):
        self._sleepVoiceObj.SpeakFromFile(self._stopInnerFile)
    
    def VoiceAwake(self):
        self._awakeVoiceObj.SpeakFromFile(self._wakeInnerFile)
    
    def VoiceWait(self):
        self._waitVoiceObj.SpeakFromFile(self._waitInnerFile)
    
    def VoiceDefault(self, content):
        if self._voice is None:
            self._voice = TextToSpeech()
        self._voice.SpeakFromText(content)
  
    def HasGreeted(self):
        return self._greeted

    def ResetWaker(self):
        self.wakeAction = None
    def ResetStopper(self):
        self.stopAction = None

    def ResetVoice(self):
        self._voice = None

    def IsIdle(self):
        return (self._voice is not None) and self._voice.Finished()

    def InitWaker(self):
        if self.wakeAction is None:
            self.wakeAction = Action(self.pv_access_key, self.wakeWordFile)
            self.wakeAction.StartListening()
       
    def InitStopper(self):
        if self.stopAction is None:
            self.stopAction = Action(self.pv_access_key, self.stopWordFile)
            self.stopAction.StartListening()


    def UseDisplay(self, text):
        txtDisplay = TextDisplay()
        txtDisplay.Display(text)

    def SetHasGreeted(self, state):
        self._greeted = state
