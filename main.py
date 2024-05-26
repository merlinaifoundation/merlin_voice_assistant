import struct
import time
from time import sleep
from decouple import config

import pvcobra

import pyaudio

import pvleopard

# NEW LIBS
from libs.textResponder import TextDisplay
from libs.textToSpeech import TextToSpeech
from libs.recorder import Recorder
from libs.gpt import ChatGPT
from libs.actions import Actions
from libs.greeter import Greeter

audio_stream = None
pa = None
wav_file = None

pv_access_key = str(config("PV_ACCESS_KEY"))

print("Using PV KEY", pv_access_key)

chatGPT = ChatGPT()

def listen():

    print("Listening...")
    cobra = pvcobra.create(access_key=pv_access_key)

    listen_pa = pyaudio.PyAudio()

    listen_audio_stream = listen_pa.open(
        rate=cobra.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=cobra.frame_length,
    )

    while True:
        listen_pcm = listen_audio_stream.read(cobra.frame_length)
        listen_pcm = struct.unpack_from("h" * cobra.frame_length, listen_pcm)

        if cobra.process(listen_pcm) > 0.3:
            print("Voice detected")
            listen_audio_stream.stop_stream()
            listen_audio_stream.close()
            cobra.delete()
            break


def detect_silence():
    cobra = pvcobra.create(access_key=pv_access_key)

    silence_pa = pyaudio.PyAudio()

    cobra_audio_stream = silence_pa.open(
        rate=cobra.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=cobra.frame_length,
    )

    last_voice_time = time.time()

    while True:
        cobra_pcm = cobra_audio_stream.read(cobra.frame_length)
        cobra_pcm = struct.unpack_from("h" * cobra.frame_length, cobra_pcm)

        if cobra.process(cobra_pcm) > 0.2:
            last_voice_time = time.time()
        else:
            silence_duration = time.time() - last_voice_time
            if silence_duration > 1.3:
                print("Text interpreted\n")
                cobra_audio_stream.stop_stream()
                cobra_audio_stream.close()
                cobra.delete()
                last_voice_time = None
                break


leopardClient = pvleopard.create(
    access_key=pv_access_key,
    enable_automatic_punctuation=True,
)


try:

    count = 0

    actionWake = None
    actionStop = None
    questionsRecorder = None
    voice = None
    welcome = True
    firstTime = True
    greeter = Greeter()

    while True:

        sleep(0.01)

        if actionWake is None:
            actionWake = Actions("WAKE_WORD_FILE")
            actionWake.Enable()

        if actionStop is None:
            actionStop = Actions("STOP_WORD_FILE")
            actionStop.Enable()

        if questionsRecorder is None:
            questionsRecorder = Recorder()

        if voice is None:
            voice = TextToSpeech()

        count += 1

        if questionsRecorder.IsRecording():
            questionsRecorder.StopRecording()

        else:

            userRecordedInput = questionsRecorder.HasRecording()
            transcriptRawSize = len(userRecordedInput)
            # print("Iter: ", count, " Idle")

            if transcriptRawSize > 0:

                response = None

                print("Iter: ", count, " has Recording Size: ", transcriptRawSize)

                questionsRecorder.CleanRecording()

                transcript, words = leopardClient.process(userRecordedInput)
                print("Transcript: ", transcript)

                response = chatGPT.Query(transcript)

                if response is None:
                    questionsRecorder = None
                else:
                    chatGPT.AppendAnswer(response)
                    voice.Tell(response)
                    txtDisplay = TextDisplay()
                    txtDisplay.Tell(response)

            else:

                if firstTime:
                    firstTime = False
                    actionWake.SetEnabled(True)

                if actionWake.IsEnabled():

                    if greeter.Idle():
                        greeter.AwakeVoice()                    
                        sleep(5)
                    
                    if not questionsRecorder.Finished():
                        questionsRecorder.StartRecording()
                        listen()
                        detect_silence()

                    if voice.Finished():
                        print("Voice Finished. Flushing...")
                        voice = None
                        questionsRecorder = None

                if actionStop.IsEnabled():

                    print("Sleeping...")
                    greeter.SleepingVoice()
                    
                    print("Flushing...")
                   
                    actionWake = None
                    questionsRecorder = None
                    actionStop = None


except KeyboardInterrupt:
    print("\nExiting ChatGPT Virtual Assistant")
    leopardClient.delete
