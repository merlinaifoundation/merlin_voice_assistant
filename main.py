# NEW LIBS
from time import sleep
from tapeRecorder.base import TapeRecorder
from libs.gpt import ChatGPT
from libs.greeter import Greeter

try:

    greeter = Greeter()
    greeter.StartThread()

    tapeRecorder = TapeRecorder(greeter)
    tapeRecorder.StartThread()
    
    
    ai = ChatGPT()

    while True:

        sleep(0.01)
        
        enabled = greeter.UserCancelled() is False and greeter.UserInvoked() is True
        
        openMicOn = enabled and greeter.IsIdle()
        tapeRecorder.SetOpenMic(openMicOn)
        
        hasRecordedStuff = enabled and tapeRecorder.fileRecording
        if hasRecordedStuff:
        
            userTranscript = ai.SpeechToText(hasRecordedStuff, "text")
            print("Transcript:", userTranscript)

            aiResponse = ai.Query(userTranscript)
            ai.AppendAnswer(aiResponse, 29)
            
            tapeRecorder.fileRecording = None

            greeter.UseVoice(aiResponse)


except Exception as error:
    print("\nExiting...", error)
