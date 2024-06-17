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
    greeter.initStopper()
    greeter.initWaker()
    # sleep(0.02)
    greeter.forceWake()

    while True:

        sleep(0.01)

        greeter.countIteration()
        print ("Doing nothing, Iter:", greeter.iteration)

        # checks if user asked to Stop
        if greeter.UserCancelled():

            #mode sleeping
            if greeter._stopMode == 1:
                print("Sleeping...")
                greeter.voiceMaker.VoiceSleeping()
            
            #mode interruption when greeter is talking
            if greeter._stopMode == 2:
                print("Processing Interruption...")
                greeter.voiceMaker.VoiceProcess()
                
            print("Flushing...")
            greeter.resetWaker()
            greeter.resetStopper()
            
            
            tapeRecorder.resetTape()
            
            print("Restarting...")
            
            
            greeter.initWaker()

            #mode sleeping
            if greeter._stopMode == 1:
                greeter.setHasGreeted(False)
            
            #mode interruption when greeter is talking
            if greeter._stopMode == 2:
                greeter.forceWake()
                
            greeter.initStopper()
            sleep(0.01)
            
            continue

        if greeter.wakeAction and greeter.wakeAction.IsInvoked():

            if not greeter.hasGreeted():
                print("Welcome...")
                greeter.voiceMaker.VoiceAwake()
                greeter.setHasGreeted(True)
                sleep(1)
                continue

            if greeter.UserCancelled():
                continue

            # check if voice finished to start recording again
            if greeter.voiceMaker.IsIdle():
                print("GreeterVoice Finished. Flushing...")
                tapeRecorder.resetTape()
                greeter._stopMode = 1
                # sleep(0.05)


            tapeRecorder.initialize()

            if greeter.UserCancelled():
                continue
            
            tapeRecorder.startTape(greeter.stopAction)

            if greeter.UserCancelled():
                continue

            tapeRecorder.stopTape()

            if greeter.UserCancelled():
                continue

            print(
                "Iter: ",
                greeter.iteration,
            )

            if tapeRecorder.Recorder:

                userRecordedInput = tapeRecorder.Recorder.GetRecordingObj()
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

                        fileRecording = tapeRecorder.Recorder.SaveRecordingObj()
                        tapeRecorder.Recorder.CleanRecording()

                        if greeter.UserCancelled():
                            continue

                        userTranscript = ai.speechToText(fileRecording, "text")
                        print("Transcript:", userTranscript)

                        if greeter.UserCancelled():
                            continue

                        aiResponse = ai.query(userTranscript)
                        ai.AppendAnswer(aiResponse, 29)

                        if greeter.UserCancelled():
                            continue

                        if aiResponse is not None:

                            if len(aiResponse) > 300:
                                greeter.voiceMaker.VoiceWait()

                            print("Display Response: ", aiResponse)
                            greeter._stopMode = 2
                            greeter.voiceMaker.VoiceDefault(aiResponse, greeter.stopAction)
                            # greeter.UseDisplay(aiResponse)
                    else:
                        print("Discarding...")
                        tapeRecorder.resetTape()

    

except Exception as error:
    print("\nExiting...", error)
