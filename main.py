# NEW LIBS
from time import sleep
from tapeRecorder.base import TapeRecorder
from libs.gpt import ChatGPT
from libs.greeter import Greeter

try:

    greeter = Greeter()
    greeter.StartThread()

    tapeRecorder = TapeRecorder(greeter)
    tapeRecorder.StartThread()
    ai = ChatGPT()

    while True:

        sleep(0.01)

        # check if voice finished to start recording again
        if tapeRecorder.fileRecording:
            # print("GreeterVoice Finished. Flushing...")

            if greeter.UserCancelled():
                continue

            userTranscript = ai.SpeechToText(tapeRecorder.fileRecording, "text")
            tapeRecorder.fileRecording = None
            print("Transcript:", userTranscript)

            if greeter.UserCancelled():
                continue

            aiResponse = ai.Query(userTranscript)
            ai.AppendAnswer(aiResponse, 29)

            if greeter.UserCancelled():
                continue

            greeter.UseVoice(aiResponse)


except Exception as error:
    print("\nExiting...", error)
