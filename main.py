from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from libs.gpt import ChatGPT
from libs.listener import Listener


try:

    greeter = Greeter()

    count = 0

    firstTimeLoading = True
    chatGPT = ChatGPT()
    listener = Listener(0.45, 2.4, 0.4)

    while True:

        greeter.InitWaker()
        sleep(0.25)
        greeter.InitStopper()
        sleep(0.25)

        if firstTimeLoading:
            firstTimeLoading = False
            if greeter.wakeAction:
                greeter.wakeAction.SetInvoked(True)
                sleep(0.05)

        # checks if user asked to Stop
        if greeter.stopAction and greeter.stopAction.IsInvoked():

            print("Sleeping...")
            greeter.VoiceSleeping()
            greeter.ResetRecorder()
            greeter.ResetWaker()
            greeter.SetHasGreeted(False)
            greeter.ResetStopper()
            print("Flush finished. Restarting...")
            sleep(0.05)
            continue

        if greeter.wakeAction and greeter.wakeAction.IsInvoked():

            if not greeter.HasGreeted():
                print("Welcome...")
                greeter.VoiceAwake()
                greeter.SetHasGreeted(True)
                sleep(0.5)
                continue

            # check if voice finished to start recording again
            if greeter.IsIdle():
                print("GreeterVoice Finished. Flushing...")
                greeter.ResetRecorder()

            greeter.InitRecorder()

            if greeter.questionsRecorder and not greeter.questionsRecorder.Finished():
                greeter.questionsRecorder.StartRecording()
                listener.Listen(greeter.stopAction)
                listener.DetectSilence(greeter.stopAction)

            if greeter.stopAction and greeter.stopAction.IsInvoked():
                continue

            if greeter.questionsRecorder and greeter.questionsRecorder.IsRecording():
                print("Stopping Recording...")
                greeter.questionsRecorder.StopRecording()

            if greeter.stopAction and greeter.stopAction.IsInvoked():
                continue

            if greeter.questionsRecorder:

                userRecordedInput = greeter.questionsRecorder.HasRecordingObj()
                userRecordedInputSize = len(userRecordedInput)

                # print("Iter: ", count, " Idle")
                if userRecordedInputSize > 0:

                    print(
                        "Iter: ", count, " has Recording Size: ", userRecordedInputSize
                    )

                    if userRecordedInputSize > 38000:

                        if greeter.stopAction and greeter.stopAction.IsInvoked():
                            continue

                        # if userRecordedInputSize > 300000:
                        #    greeter.VoiceProcess()
                        #
                        fileRecording = greeter.questionsRecorder.SaveRecordingObj()
                        greeter.questionsRecorder.CleanRecording()

                        if greeter.stopAction and greeter.stopAction.IsInvoked():
                            continue

                        aiResponse = None
                        transcript = greeter.SpeechToText(fileRecording)
                        print("Transcript:", transcript)

                        if greeter.stopAction and greeter.stopAction.IsInvoked():
                            continue

                        aiResponse = chatGPT.Query(transcript)

                        if greeter.stopAction and greeter.stopAction.IsInvoked():
                            continue

                        if aiResponse is not None:

                            if len(aiResponse) > 300:
                                greeter.VoiceWait()

                            chatGPT.AppendAnswer(aiResponse)

                            print("Display Response: ", aiResponse)
                            greeter.VoiceDefault(aiResponse, greeter.stopAction)
                            # greeter.UseDisplay(aiResponse)
                    else:
                        print("Discarding...")
                        greeter.ResetRecorder()

        if count > 1000000:
            count = 0
        count += 1
        sleep(0.1)

except Exception as error:
    print("\nExiting ChatGPT Virtual Assistant", error)
