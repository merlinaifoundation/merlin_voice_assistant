from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from tapeRecorder.base import TapeRecorder
from libs.gpt import ChatGPT

try:

    greeter = Greeter()
    tapeRecorder = TapeRecorder()
    ai = ChatGPT()

    # sleep(0.02)
    greeter.InitStopper()
    greeter.InitWaker()
    # sleep(0.02)
    greeter.ForceWake()

    while True:

        sleep(0.01)

        greeter.CountIteration()
        print ("Doing nothing, Iter:", greeter.count)

        # checks if user asked to Stop
        if greeter.UserCancelled():

            #mode sleeping
            if greeter.stopMode == 1:
                print("Sleeping...")
                greeter.voiceMaker.VoiceSleeping()
            
            #mode interruption when greeter is talking
            if greeter.stopMode == 2:
                print("Processing Interruption...")
                greeter.voiceMaker.VoiceProcess()
                
            print("Flushing...")
            greeter.ResetWaker()
            greeter.ResetStopper()
            
            
            tapeRecorder.Reset()
            
            print("Restarting...")
            
            
            greeter.InitWaker()

            #mode sleeping
            if greeter.stopMode == 1:
                greeter.SetHasGreeted(False)
            
            #mode interruption when greeter is talking
            if greeter.stopMode == 2:
                greeter.ForceWake()
                
            greeter.InitStopper()
            sleep(0.01)
            
            continue

        if greeter.wakeAction and greeter.wakeAction.IsInvoked():

            if not greeter.HasGreeted():
                print("Welcome...")
                greeter.voiceMaker.VoiceAwake()
                greeter.SetHasGreeted(True)
                sleep(1)
                continue

            if greeter.UserCancelled():
                continue

            # check if voice finished to start recording again
            if greeter.voiceMaker.IsIdle():
                print("GreeterVoice Finished. Flushing...")
                tapeRecorder.Reset()
                greeter.stopMode = 1
                # sleep(0.05)


            tapeRecorder.Initialize()

            if greeter.UserCancelled():
                continue
            
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
                                greeter.voiceMaker.VoiceWait()

                            print("Display Response: ", aiResponse)
                            greeter.stopMode = 2
                            greeter.voiceMaker.VoiceDefault(aiResponse, greeter.stopAction)
                            # greeter.UseDisplay(aiResponse)
                    else:
                        print("Discarding...")
                        tapeRecorder.Reset()

    

except Exception as error:
    print("\nExiting...", error)
