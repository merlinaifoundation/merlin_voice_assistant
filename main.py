from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from hearer.base import Hearer
from libs.gpt import ChatGPT

try:

    greeter = Greeter()
    hearer = Hearer()
    ai = ChatGPT()

    greeter.InitStopper()
    greeter.InitWaker()
    greeter.WakeOnFirstLoad()
    
        
    while True:

        sleep(0.2)

        greeter.CountIteration()

        # checks if user asked to Stop
        if greeter.UserCancelled():

            print("Sleeping...")
            greeter.VoiceSleeping()
            print("Flushing...")
            greeter.ResetWaker()
            greeter.SetHasGreeted(False)
            hearer.ResetRecorder()
            greeter.ResetStopper()
            #
            print("Restarting...")
            greeter.InitWaker()
            sleep(0.05)
            greeter.InitStopper()
            sleep(0.05)
            continue

        if greeter.wakeAction and greeter.wakeAction.IsInvoked():

            if not greeter.HasGreeted():
                print("Welcome...")
                greeter.VoiceAwake()
                greeter.SetHasGreeted(True)
                sleep(1)
                # continue

            if greeter.UserCancelled():
                continue

            # check if voice finished to start recording again
            if greeter.IsIdle():
                print("GreeterVoice Finished. Flushing...")
                hearer.ResetRecorder()
                sleep(0.05)

            hearer.InitRecorder()

            if hearer.recorder and not hearer.recorder.Finished():
                hearer.recorder.StartRecording()
                hearer.listener.Listen(greeter.stopAction)
                hearer.listener.DetectSilence(greeter.stopAction)

            if greeter.UserCancelled():
                continue

            if hearer.recorder and hearer.recorder.IsRecording():
                print("Stopping Recording...")
                hearer.recorder.StopRecording()

            if greeter.UserCancelled():
                continue

            if hearer.recorder:

                userRecordedInput = hearer.recorder.HasRecordingObj()
                userRecordedInputSize = len(userRecordedInput)

                print(
                        "Iter: ",
                        greeter.count,
                        " has Recording Size: ",
                        userRecordedInputSize,
                    )
                
                if userRecordedInputSize > 0:

                    if userRecordedInputSize > 38000:

                        if greeter.UserCancelled():
                            continue

                        # if userRecordedInputSize > 300000:
                        #    greeter.VoiceProcess()
                        #
                        fileRecording = hearer.recorder.SaveRecordingObj()
                        hearer.recorder.CleanRecording()

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
                        hearer.ResetRecorder()


except Exception as error:
    print("\nExiting...", error)
