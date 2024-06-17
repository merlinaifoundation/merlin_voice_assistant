# NEW LIBS
from time import sleep
from tapeRecorder.base import TapeRecorder
from ai.gpt import ChatGPT
from libs.greeter import Greeter

try:

    greeter = Greeter()
    greeter.StartThread()

    tapeRecorder = TapeRecorder(greeter)
    tapeRecorder.StartThread()

    brain = ChatGPT()
    brain.StartThread()

    while True:

        sleep(0.01)

        enabled = greeter.UserInvoked()
        cancelled = greeter.UserCancelled()
        idle = greeter.IsIdle()
        openMicOn = idle and enabled

        status = int(enabled), int(cancelled), int(idle), int(openMicOn)
        # print("\nSTATUS", status)

        # bypass filter when cancelling!
        bypassFilter = cancelled
        tapeRecorder.SetBypassFilter(bypassFilter)

        # not finished the flags-implementation
        tapeRecorder.SetCancelled(cancelled)

        # to start recording session
        tapeRecorder.SetOpenMic(openMicOn)

        cancelled = greeter.UserCancelled()

        brain.MakeSummary(cancelled)

        # has record to process for answers?
        # brain.SetResponse(None)

        fileRecording = tapeRecorder.GetTape()

        brain.SetQuery(fileRecording)

        #tapeRecorder.SetTape(None)
        tapeRecorder.SetTape(None)
        
        aiResponse = brain.GetResponse()
        greeter.VoiceResponse(aiResponse)

        if greeter.IsIdle():
            if aiResponse:
                brain.SetResponse(None)
                tapeRecorder.resetTape()

        #


except Exception as error:
    print("\nExiting...", error)
