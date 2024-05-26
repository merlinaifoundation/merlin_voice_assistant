
from time import sleep

# NEW LIBS
from libs.greeter import Greeter
from libs.recorder import Recorder
from libs.gpt import ChatGPT
from libs.listener import Listener
from libs.interpreter import Interpreter


try:

    count = 0

    questionsRecorder = None
    firstTimeLoading = True
    greeter = Greeter()
    chatGPT = ChatGPT()
    interpreter = Interpreter()
    
                    
    while True:

        sleep(0.1)

        greeter.InitActions()
        
        if firstTimeLoading:
            firstTimeLoading = False
            if greeter.wakeAction:
                greeter.wakeAction.SetInvoked(True)

        # check if voice finished to start recording again
        if greeter.IsIdle():
            print("GreeterVoice Finished. Flushing...")
            greeter.ResetVoice()
            questionsRecorder = None
        
        if questionsRecorder is None:
            questionsRecorder = Recorder(None)

        count += 1

        if questionsRecorder.IsRecording():
            print("Stopping Recording...")
            questionsRecorder.StopRecording()

        userRecordedInput = questionsRecorder.HasRecording()
        transcriptRawSize = len(userRecordedInput)
        # print("Iter: ", count, " Idle")

        if transcriptRawSize > 0:

            response = None

            print("Iter: ", count, " has Recording Size: ", transcriptRawSize)
            
            questionsRecorder.CleanRecording()
            transcript  = interpreter.SpeechToText(userRecordedInput)
            
            response = chatGPT.Query(transcript)

            if response is None:
                questionsRecorder = None
            else:
                
                chatGPT.AppendAnswer(response)

                greeter.UseVoice(response)

                greeter.UseDisplay(response)

        else:

            if greeter.wakeAction and greeter.wakeAction.IsInvoked():
                # check if has welcomed the user
                if not greeter.HasGreeted():
                    print("Welcoming...")
                    greeter.AwakeVoice()
                    greeter.SetHasGreeted(True)
                    sleep(3)
                if questionsRecorder and not questionsRecorder.Finished():
                    questionsRecorder.StartRecording()
                    listener = Listener()
                    listener.Trigger()

            # checks if user asked to Stop
            if greeter.stopAction and greeter.stopAction.IsInvoked():

                greeter.ResetActions()
                greeter.ResetVoice()
                questionsRecorder = None
                
                print("Sleeping...")
                greeter.SleepingVoice()
                greeter.SetHasGreeted(False)
                print("Flushing...")
                
                


except KeyboardInterrupt:
    print("\nExiting ChatGPT Virtual Assistant")
