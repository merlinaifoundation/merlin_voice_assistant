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

        status = int(enabled), int(cancelled), int(idle),  int(openMicOn)
        #integer = bytes(status) #.decode("utf-8")
        #print("\nSTATUS", status)

        tapeRecorder.SetOpenMic(openMicOn)

        #hasRecordedStuff = enabled and tapeRecorder.fileRecording
        hasRecordedStuff =  tapeRecorder.fileRecording

        if hasRecordedStuff:

            userTranscript = ai.SpeechToText(hasRecordedStuff, "text")
            print("Transcript:", userTranscript)

            aiResponse = ai.Query(userTranscript)
            ai.AppendAnswer(aiResponse, 29)

            tapeRecorder.fileRecording = None

            greeter.UseVoice(aiResponse)


except Exception as error:
    print("\nExiting...", error)
