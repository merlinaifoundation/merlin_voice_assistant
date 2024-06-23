from threading import Thread
import time
from decouple import config

from libs.textToSpeech import TextToSpeech


class VoiceMaker(Thread):

    def __init__(self):
        super().__init__()
        self.name = 'VoiceMaker'

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

        self._initVoiceObj = TextToSpeech()
        self._processVoiceObj = TextToSpeech()
        self._awakeVoiceObj = TextToSpeech()
        self._sleepingVoicObj = TextToSpeech()
        self._defaultVoiceObj = TextToSpeech()
        self._waitVoiceObj = TextToSpeech()
        
        self._prepareDefaultVoices()

        diff = round(time.time() - timeNow, 2)
        self._prGreen("VoiceMaker Creation in seconds: ", diff)

    def _prRed(self, skk, number):
        print("\033[91m {}\033[00m".format(skk), number)

    def _prGreen(self, skk, number):
        print("\033[92m {}\033[00m".format(skk), number)


    def _prepareDefaultVoices(self):

        print("Initializing...")
        self.CreateInitVoice(self.initVoiceTxt)
        self.VoiceInit()
        self.CreateProcessVoice(self.processVoiceTxt)
        self.CreateWaitVoice(self.waitVoiceTxt)
        self.VoiceWait()
        self.CreateSleepVoice(self.sleepingVoiceTxt)
        self.CreateWakeVoice(self.awakeVoiceTxt)
        self.VoiceDefault("Almost there!")
        print("Finished creating the TTS Defaults")
        
        
    def CreateInitVoice(self, txt, force = False):

        if self._initVoiceObj.SetFile(self._initInnerFile) is False or force:
            self._initVoiceObj.PrepareFileFromText(txt)
            print("Created Init Audio File...")

    def CreateProcessVoice(self, txt, force = False):
        if self._processVoiceObj.SetFile(self._processInnerFile) is False or force:
            self._processVoiceObj.PrepareFileFromText(txt)
            print("Created Process Audio File...")
            
    def CreateWaitVoice(self, txt, force = False):
        if self._waitVoiceObj.SetFile(self._waitInnerFile) is False or force:
            self._waitVoiceObj.PrepareFileFromText(txt)
            print("Creating Wait Audio File...")
        
    def CreateWakeVoice(self, txt, force = False):
        if self._awakeVoiceObj.SetFile(self._awakeInnerFile) is False or force:
            self._awakeVoiceObj.PrepareFileFromText(txt)
            print("Created Wake Audio File...")
            
            #self._awakeVoiceObj = TextToSpeech()
    def CreateSleepVoice(self, txt,  force = False):
        if self._sleepingVoicObj.SetFile(self._sleepingInnerFile) is False or force:
            self._sleepingVoicObj.PrepareFileFromText(txt)
            print("Created Stop Audio File...")
    
    def VoiceSleeping(self, asThread = True):
        # self._awakeVoiceObj = TextToSpeech()
        if  self._sleepingVoicObj:
            self._sleepingVoicObj = TextToSpeech()
        self._sleepingVoicObj.SpeakFromFile(self._sleepingInnerFile, asThread)

    def VoiceAwake(self, asThread = True):
        # self._awakeVoiceObj = TextToSpeech()
        if  self._awakeVoiceObj:
            self._awakeVoiceObj = TextToSpeech()
        self._awakeVoiceObj.SpeakFromFile(self._awakeInnerFile, asThread)

    def VoiceWait(self, asThread = True):
        # self._waitVoiceObj = TextToSpeech()
        if self._waitVoiceObj:
            self._waitVoiceObj = TextToSpeech()
        self._waitVoiceObj.SpeakFromFile(self._waitInnerFile, asThread)

    def VoiceProcess(self, asThread = True):
        if self._processVoiceObj:
            self._processVoiceObj = TextToSpeech()
        self._processVoiceObj.SpeakFromFile(self._processInnerFile, asThread)

    def VoiceInit(self, asThread = False):

        if  self._initVoiceObj:
            self._initVoiceObj = TextToSpeech()
        self._initVoiceObj.SpeakFromFile(self._initInnerFile, asThread)

    def SetCancelled(self, cancelled):
        self._defaultVoiceObj.SetCancelled(cancelled)
    
    def VoiceDefault(self, content,asThread = True):
        if self._defaultVoiceObj:
            self._defaultVoiceObj = TextToSpeech()
        self._defaultVoiceObj.SpeakFromText(content,asThread)

    def IsIdle(self):
        condition1 = self._defaultVoiceObj and self._defaultVoiceObj.Finished()
        condition2 = self._awakeVoiceObj  and self._awakeVoiceObj.Finished()
        condition3 = self._waitVoiceObj  and self._waitVoiceObj.Finished()
        condition5 = self._initVoiceObj  and self._initVoiceObj.Finished()
        condition4 = self._processVoiceObj  and self._processVoiceObj.Finished()
        condition6 = self._sleepingVoicObj  and self._sleepingVoicObj.Finished()

        #print(condition1, condition2)
        return condition1 and condition2 and condition3 and condition4 and condition5 and condition6
