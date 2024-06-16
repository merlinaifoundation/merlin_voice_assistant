from threading import Thread
import time
from decouple import config

from libs.textToSpeech import TextToSpeech


class VoiceMaker(Thread):

    def __init__(self):
        super().__init__()
        timeNow = time.time()

        self.sleepingVoiceTxt = config("SLEEPING_VOICE")
        self.awakeVoiceTxt = config("AWAKE_VOICE")
        self.waitVoiceTxt = config("WAIT_VOICE")
        self.initVoiceTxt = config("INIT_VOICE")
        self.processVoiceTxt = config("PROCESSING_VOICE")
        self._sleepingInnerFile = "StopVoice.mp3"
        self._awakeInnerFile = "WakeVoice.mp3"
        self._waitInnerFile = "WaitVoice.mp3"
        self._initInnerFile = "InitVoice.mp3"
        self._processInnerFile = "ProcessVoice.mp3"

        self._prepareInitialVoice()
        self._prepareDefaultVoices()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("VoiceMaker Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[91m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number)

    def _prepareInitialVoice(self):

        self._initVoiceObj = TextToSpeech()
        if self._initVoiceObj.SetFile(self._initInnerFile) is False:
            self._initVoiceObj.PrepareFileFromText(self.initVoiceTxt, False)
        print("Initializing...")
        self.VoiceInit()

    def _prepareDefaultVoices(self):


        self._waitVoiceObj = TextToSpeech()
        if self._waitVoiceObj.SetFile(self._processInnerFile) is False:
            self._waitVoiceObj.PrepareFileFromText(self.processVoiceTxt, False)
            print("Created Process Audio File...")
            
        #self._waitVoiceObj = TextToSpeech()
        if self._waitVoiceObj.SetFile(self._waitInnerFile) is False:
            self._waitVoiceObj.PrepareFileFromText(self.waitVoiceTxt, False)
            print("Creating Wait Audio File...")
        self.VoiceWait()

        
        self._awakeVoiceObj = TextToSpeech()
        
        self.CreateSleepVoice(self.sleepingVoiceTxt)

        self.CreateWakeVoice(self.awakeVoiceTxt)
        
        self._defaultVoiceObj = TextToSpeech()
        self.VoiceDefault("Almost there!", None)
        print("Finished creating the TTS Defaults")

    def CreateWakeVoice(self, txt, force = False):
        if self._awakeVoiceObj.SetFile(self._awakeInnerFile) is False or force:
            self._awakeVoiceObj.PrepareFileFromText(txt, False)
            print("Created Wake Audio File...")
            
            #self._awakeVoiceObj = TextToSpeech()
    def CreateSleepVoice(self, txt,  force = False):
        if self._awakeVoiceObj.SetFile(self._sleepingInnerFile) is False or force:
            self._awakeVoiceObj.PrepareFileFromText(txt, False)
            print("Created Stop Audio File...")
            #self._awakeVoiceObj = TextToSpeech()
        
    
    def VoiceSleeping(self):
        # self._awakeVoiceObj = TextToSpeech()
        self._awakeVoiceObj.SpeakFromFile(self._sleepingInnerFile, False)

    def VoiceAwake(self):
        # self._awakeVoiceObj = TextToSpeech()
        self._awakeVoiceObj.SpeakFromFile(self._awakeInnerFile, False)

    def VoiceWait(self):
        # self._waitVoiceObj = TextToSpeech()
        self._waitVoiceObj.SpeakFromFile(self._waitInnerFile, False)

    def VoiceProcess(self):
        # self._processVoiceObj = TextToSpeech()
        self._waitVoiceObj.SpeakFromFile(self._processInnerFile, False)

    def VoiceInit(self):

        # self._initVoiceObj = TextToSpeech()
        self._initVoiceObj.SpeakFromFile(self._initInnerFile, False)

    def VoiceDefault(self, content, stopObj):

        # self._defaultVoiceObj = TextToSpeech()
        self._defaultVoiceObj.SetForceStopObj(stopObj)
        self._defaultVoiceObj.SpeakFromText(content, False)

    def IsIdle(self):
        condition1 = (self._defaultVoiceObj is not None) and self._defaultVoiceObj.Finished()
        condition2 = (self._awakeVoiceObj is not None) and self._awakeVoiceObj.Finished()
        condition3 = (self._waitVoiceObj is not None) and self._waitVoiceObj.Finished()

        #print(condition1, condition2)
        return condition1 and condition2 and condition3
