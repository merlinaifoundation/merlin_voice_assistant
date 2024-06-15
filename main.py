
# NEW LIBS
from time import sleep
from tapeRecorder.base import TapeRecorder
from libs.gpt import ChatGPT
from libs.runner import RunnerGreeter

try:

    tapeRecorder = TapeRecorder()
    ai = ChatGPT()

    runnerGreet = RunnerGreeter()
    
    runnerGreet.start()

    while True:
        
        sleep(0.01)

        #print ("Doing nothing, Iter:", greeter.count)

        if runnerGreet.greeter.UserInvoked():

            # check if voice finished to start recording again
            if runnerGreet.greeter.voiceMaker.IsIdle():
                #print("GreeterVoice Finished. Flushing...")
                tapeRecorder.Reset()
                #runnerGreet.greeter.stopMode = 1

            tapeRecorder.Initialize()

            if runnerGreet.greeter.UserCancelled():
                continue
            
            tapeRecorder.Start(runnerGreet.greeter.stopAction)

            if runnerGreet.greeter.UserCancelled():
                continue

            tapeRecorder.Stop()

            if runnerGreet.greeter.UserCancelled():
                continue

            if tapeRecorder.recorder:

                userRecordedInput = tapeRecorder.recorder.HasRecordingObj()
                userRecordedInputSize = len(userRecordedInput)

                print(
                    "Recording Size: ",
                    userRecordedInputSize,
                )

                if userRecordedInputSize > 0:

                    if userRecordedInputSize > 38000:

                        if runnerGreet.greeter.UserCancelled():
                            continue

                        # if userRecordedInputSize > 300000:
                        #    greeter.VoiceProcess()
                        #

                        fileRecording = tapeRecorder.recorder.SaveRecordingObj()
                        tapeRecorder.recorder.CleanRecording()

                        if runnerGreet.greeter.UserCancelled():
                            continue

                        userTranscript = ai.SpeechToText(fileRecording, "text")
                        print("Transcript:", userTranscript)

                        if runnerGreet.greeter.UserCancelled():
                            continue

                        aiResponse = ai.Query(userTranscript)
                        ai.AppendAnswer(aiResponse, 29)

                        if runnerGreet.greeter.UserCancelled():
                            continue

                        runnerGreet.SetContent(aiResponse)
                        
                        
                    else:
                        print("Discarding...")
                        tapeRecorder.Reset()
    

except Exception as error:
    print("\nExiting...", error)
