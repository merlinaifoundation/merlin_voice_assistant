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

        enabled = greeter.UserInvoked()
        cancelled = greeter.UserCancelled()

        idle = greeter.IsIdle()
        openMicOn = not cancelled and enabled and idle

        status = int(enabled), int(cancelled), int(idle), int(openMicOn)
        # integer = bytes(status) #.decode("utf-8")
        # print("\nSTATUS", status)

        tapeRecorder.SetOpenMic(openMicOn)
        
        cancelled = greeter.UserCancelled()

        # hasRecordedStuff = enabled and tapeRecorder.fileRecording
        hasRecordedStuff = tapeRecorder.fileRecording

        if hasRecordedStuff:

            userTranscript =None
            role = "user"
            if not cancelled:
                userTranscript = ai.SpeechToText(hasRecordedStuff, "text")
                print("Transcript:", userTranscript)
            else:
                userTranscript = ai.GetBriefer()
                role = "system"
            
            #ai.AppendToList(userTranscript, "user", 29)
                
            aiResponse = ai.Query(userTranscript, role)

            if not cancelled:
                ai.AppendToList(userTranscript, "user", 29)
                ai.AppendToList(aiResponse, "assistant", 29)
                greeter.UseVoice(aiResponse)
            else:
                ai.ClearCummulativeList()
                appendTopics = "Our last conversation was about: " + str(aiResponse)
                ai.AppendToList(
                    appendTopics,
                    "system",
                    29,
                )
                greeter.voiceMaker.CreateWakeVoice(appendTopics, True)

            tapeRecorder.fileRecording = None


except Exception as error:
    print("\nExiting...", error)
