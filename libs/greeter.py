from threading import Thread
from decouple import config

from libs.actions import Action
from libs.textToSpeech import TextToSpeech
from libs.textResponder import TextDisplay
from libs.interpreter import InterpreterAI
from libs.recorder import Recorder


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

        self._stopInnerFile = "StopVoice.mp3"
        self._wakeInnerFile = "WakeVoice.mp3"
        self._waitInnerFile = "WaitVoice.mp3"
        self._initInnerFile = "InitVoice.mp3"
        self._processInnerFile = "ProcessVoice.mp3"

        self.questionsRecorder = None
        
        self._prepareInitialVoice()
        self._prepareDefaultVoices()

        self.wakeAction = None
        self.stopAction = None
        self._greeted = False

        self.interpreter = InterpreterAI()

    def SpeechToText(self, userRecordedInput):
        transcript = self.interpreter.SpeechToText(userRecordedInput, "text")
        return transcript

    def _prepareInitialVoice(self):

        self._initVoiceObj = TextToSpeech()
        self._initVoiceObj.SetFile(self._initInnerFile)
        self._initVoiceObj.PrepareFileFromText(self.initVoiceTxt)
        print("Initializing...")
        self.VoiceInit()

    def _prepareDefaultVoices(self):

        self._defaultVoiceObj = TextToSpeech()
            
        self._waitVoiceObj = TextToSpeech()
        self._waitVoiceObj.SetFile(self._waitInnerFile)
        self._waitVoiceObj.PrepareFileFromText(self.waitVoiceTxt)
        print("Creating Wait Audio File...")
        self.VoiceWait()
        
        self._processVoiceObj = TextToSpeech()
        self._processVoiceObj.SetFile(self._processInnerFile)
        self._processVoiceObj.PrepareFileFromText(self.processVoiceTxt)
        print("Creating Process Audio File...")
        
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

                
    def ResetRecorder(self):
        if self.questionsRecorder is not None:
                    if self.questionsRecorder.IsRecording():
                        print("Stopping Recording...")
                        self.questionsRecorder.StopRecording()
                    self.questionsRecorder.CleanRecording()
                    self.questionsRecorder = None

    def IsIdle(self):
        return (self._defaultVoiceObj is not None) and self._defaultVoiceObj.Finished()

    def InitRecorder(self):
        if self.questionsRecorder is None:
                self.questionsRecorder = Recorder(None)
                
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
