from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from libs.recorder import Recorder
from libs.gpt import ChatGPT
from libs.listener import Listener


try:

    count = 0

    questionsRecorder = None
    firstTimeLoading = True
    greeter = Greeter()
  
    
    chatGPT = ChatGPT()

    while True:

        greeter.InitWaker()
        sleep(0.05)

        greeter.InitStopper()
        sleep(0.05)

        if count > 1000000:
            count = 0

        count += 1

        # checks if user asked to Stop
        if greeter.stopAction and greeter.stopAction.IsInvoked():

            print("Sleeping...")
            greeter.SleepingVoice()
            greeter.ResetWaker()
            greeter.SetHasGreeted(False)
            greeter.ResetVoice()
            if questionsRecorder is not None:
                questionsRecorder.StopRecording()
                questionsRecorder.CleanRecording()
                questionsRecorder = None
            sleep(0.1)
            greeter.ResetStopper()
            print("Flush finished. Restarting...")

        else:

            if firstTimeLoading:
                firstTimeLoading = False
                if greeter.wakeAction:
                    greeter.wakeAction.SetInvoked(True)

            if greeter.wakeAction and greeter.wakeAction.IsInvoked():

                if not greeter.HasGreeted():
                    print("Welcoming...")
                    greeter.AwakeVoice()
                    greeter.SetHasGreeted(True)
                    sleep(2)

                if greeter.stopAction and greeter.stopAction.IsInvoked():
                    continue
                # check if voice finished to start recording again
                if greeter.IsIdle():
                    print("GreeterVoice Finished. Flushing...")
                    greeter.ResetVoice()
                    questionsRecorder = None

                if questionsRecorder is None:
                    questionsRecorder = Recorder(None)

                if questionsRecorder and not questionsRecorder.Finished():
                    sleep(0.1)
                    questionsRecorder.StartRecording()
                    listener = Listener()
                    listener.Trigger()

                if questionsRecorder.IsRecording():
                    print("Stopping Recording...")
                    questionsRecorder.StopRecording()

                if greeter.stopAction and greeter.stopAction.IsInvoked():
                    continue

                userRecordedInput = questionsRecorder.HasRecordingObj()
                userRecordedInputSize = len(userRecordedInput)
                # print("Iter: ", count, " Idle")
                if userRecordedInputSize > 0:

                    if greeter.stopAction and greeter.stopAction.IsInvoked():
                        continue

                    fileRecording = questionsRecorder.SaveRecordingObj()
                    print(
                        "Iter: ", count, " has Recording Size: ", userRecordedInputSize
                    )
                    

                    if greeter.stopAction and greeter.stopAction.IsInvoked():
                        continue

                    questionsRecorder.CleanRecording()
                    aiResponse = None
                    transcript = greeter.SpeechToText(fileRecording)
                    print("Transcript:", transcript)
                    aiResponse = chatGPT.Query(transcript)

                    if greeter.stopAction and greeter.stopAction.IsInvoked():
                        continue

                    if aiResponse is not None:
                        print("Display:", aiResponse)
                        chatGPT.AppendAnswer(aiResponse)
                        greeter.UseVoice(aiResponse)
                        #greeter.UseDisplay(aiResponse)
                        


except KeyboardInterrupt:
    print("\nExiting ChatGPT Virtual Assistant")

