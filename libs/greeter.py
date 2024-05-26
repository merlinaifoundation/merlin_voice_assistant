from threading import Thread
from decouple import config

from libs.textToSpeech import TextToSpeech


class Greeter(Thread):

    def __init__(self):
        super().__init__()

        self._isIdle = True
        self.sleepingVoice = config("SLEEPING_VOICE")
        self.awakeVoice = config("AWAKE_VOICE")

    def SleepingVoice(self):
        voice2 = TextToSpeech()
        voice2.Tell(self.sleepingVoice)
        self._isIdle = True
    def Idle(self):
        return self._isIdle
    def AwakeVoice(self):
        voice2 = TextToSpeech()
        voice2.Tell(self.awakeVoice)
        self._isIdle = False
