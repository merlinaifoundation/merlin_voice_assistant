from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from libs.recorder import Recorder
from libs.gpt import ChatGPT
from libs.listener import Listener


try:
    
    greeter = Greeter()
    
    count = 0
    questionsRecorder = None
    firstTimeLoading = True
    chatGPT = ChatGPT()

    while True:

        greeter.InitWaker()
        sleep(0.2)
        greeter.InitStopper()
        sleep(0.2)
        
        if firstTimeLoading:
            firstTimeLoading = False
            if greeter.wakeAction:
                greeter.wakeAction.SetInvoked(True)
                sleep(0.05)

        # checks if user asked to Stop
        if greeter.stopAction and greeter.stopAction.IsInvoked():

            print("Sleeping...")
            greeter.ResetVoice()
            greeter.VoiceSleeping()
            
            if questionsRecorder is not None:
                questionsRecorder.StopRecording()
                questionsRecorder.CleanRecording()
                questionsRecorder = None
            
            greeter.ResetWaker()
            greeter.SetHasGreeted(False)
            greeter.ResetStopper()
            print("Flush finished. Restarting...")
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
                greeter.ResetVoice()
                questionsRecorder = None

            if questionsRecorder is None:
                questionsRecorder = Recorder(None)

            if questionsRecorder and not questionsRecorder.Finished():
                questionsRecorder.StartRecording()
                listener = Listener()
                listener.Trigger()
                
            if greeter.stopAction and greeter.stopAction.IsInvoked():
                continue

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
                print("Iter: ", count, " has Recording Size: ", userRecordedInputSize)
                questionsRecorder.CleanRecording()
                
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
                    chatGPT.AppendAnswer(aiResponse)
                
                if aiResponse is not None:
                    print("Display Response:", aiResponse)
                    greeter.VoiceDefault(aiResponse, greeter.stopAction )
                    # greeter.UseDisplay(aiResponse)
                    
        
        if count > 1000000:
            count = 0
        count += 1
        sleep(0.1)

except Exception as error:
    print("\nExiting ChatGPT Virtual Assistant", error)
