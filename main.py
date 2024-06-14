from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from tapeRecorder.base import TapeRecorder
from libs.gpt import ChatGPT

try:

    greeter = Greeter()
    tapeRecorder = TapeRecorder()
    ai = ChatGPT()

    greeter.InitStopper()
    # sleep(0.02)
    greeter.InitWaker()
    # sleep(0.02)
    greeter.WakeOnFirstLoad()

    while True:

        sleep(0.25)

        greeter.CountIteration()

        # checks if user asked to Stop
        if greeter.UserCancelled():

            print("Sleeping...")
            greeter.VoiceSleeping()
            print("Flushing...")
            greeter.ResetWaker()
            greeter.SetHasGreeted(False)
            greeter.ResetStopper()
            tapeRecorder.Reset()
            #
            print("Restarting...")
            greeter.InitWaker()
            # sleep(0.02)
            greeter.InitStopper()
            sleep(0.25)
            continue

        if greeter.wakeAction and greeter.wakeAction.IsInvoked():

            if not greeter.HasGreeted():
                print("Welcome...")
                greeter.VoiceAwake()
                greeter.SetHasGreeted(True)
                sleep(1)
                continue

            if greeter.UserCancelled():
                continue

            # check if voice finished to start recording again
            if greeter.IsIdle():
                print("GreeterVoice Finished. Flushing...")
                tapeRecorder.Reset()
                # sleep(0.05)

            tapeRecorder.Initialize()

            tapeRecorder.Start(greeter.stopAction)

            if greeter.UserCancelled():
                continue

            tapeRecorder.Stop()

            if greeter.UserCancelled():
                continue

            print(
                    "Iter: ",
                    greeter.count,
                )
            
            if tapeRecorder.recorder:

                userRecordedInput = tapeRecorder.recorder.HasRecordingObj()
                userRecordedInputSize = len(userRecordedInput)
                
                print(
                    "Recording Size: ",
                    userRecordedInputSize,
                )

                if userRecordedInputSize > 0:

                    if userRecordedInputSize > 38000:

                        if greeter.UserCancelled():
                            continue

                        # if userRecordedInputSize > 300000:
                        #    greeter.VoiceProcess()
                        #
                        fileRecording = tapeRecorder.recorder.SaveRecordingObj()
                        tapeRecorder.recorder.CleanRecording()

                        if greeter.UserCancelled():
                            continue

                        userTranscript = ai.SpeechToText(fileRecording, "text")
                        print("Transcript:", userTranscript)

                        if greeter.UserCancelled():
                            continue

                        aiResponse = ai.Query(userTranscript)
                        ai.AppendAnswer(aiResponse, 29)

                        if greeter.UserCancelled():
                            continue

                        if aiResponse is not None:

                            if len(aiResponse) > 300:
                                greeter.VoiceWait()

                            print("Display Response: ", aiResponse)
                            greeter.VoiceDefault(aiResponse, greeter.stopAction)
                            # greeter.UseDisplay(aiResponse)
                    else:
                        print("Discarding...")
                        tapeRecorder.Reset()


except Exception as error:
    print("\nExiting...", error)
