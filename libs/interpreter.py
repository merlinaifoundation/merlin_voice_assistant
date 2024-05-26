from threading import Thread
from decouple import config
import pvleopard


class Interpreter(Thread):

    def __init__(self):
        super().__init__()

        pv_access_key = str(config("PV_ACCESS_KEY"))
        # print("Using PV KEY", pv_access_key)

        self.leopardClient = pvleopard.create(
            access_key=pv_access_key,
            enable_automatic_punctuation=True,
        )

    def SpeechToText(self, userRecordedInput):
        transcript = ""
        words = []
        transcriptRawSize = len(userRecordedInput)
        #print("Interpreting")
        if transcriptRawSize > 0:
            print("Has Recording Size: ", transcriptRawSize)
            transcript, words = self.leopardClient.process(userRecordedInput)
            print("Transcript: ", transcript, len(words))
            
        return transcript 
        
