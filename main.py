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
        openMicOn =  idle and enabled

        status = int(enabled), int(cancelled), int(idle), int(openMicOn)
        # print("\nSTATUS", status)
        bypassFilter = cancelled

        tapeRecorder.SetBypassFilter(bypassFilter)
        tapeRecorder.SetCancelled(cancelled)
        tapeRecorder.SetOpenMic(openMicOn)

        cancelled = greeter.UserCancelled()

        brain.MakeSummary(cancelled)

        #has record to process for answers?
        fileRecording = tapeRecorder.GetTape()
        brain.SetQuery(fileRecording)
        aiResponse = brain.GetResponse()

        if aiResponse:
            if not cancelled:
                greeter.UseVoice(aiResponse)
            else:
                greeter.voiceMaker.CreateWakeVoice(aiResponse, True)

        brain.SetResponse(None)
        tapeRecorder.SetTape(None)


except Exception as error:
    print("\nExiting...", error)
