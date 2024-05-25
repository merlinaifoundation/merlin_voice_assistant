import struct
import threading
import time
from time import sleep
from decouple import config
from colorama import Fore
import random

import openai

import pvcobra

import pyaudio

import pvleopard

# NEW LIBS
from textResponder import TextDisplay
from textToSpeech import TextToSpeech
from recorder import Recorder
from gpt import ChatGPT
from actions import Actions

audio_stream = None
pa = None
wav_file = None

pv_access_key = str(config("PV_ACCESS_KEY"))

print("Using PV KEY", pv_access_key)

chatGPT = ChatGPT()


def listen():

    print("starting Listen function")
    cobra = pvcobra.create(access_key=pv_access_key)

    listen_pa = pyaudio.PyAudio()

    listen_audio_stream = listen_pa.open(
        rate=cobra.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=cobra.frame_length,
    )

    print("Listening...")

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
                print("End of query detected\n")
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
    answerRecorder = None
    voice = None
    firstTime = True

    while True:

        if actionWake is None:
            actionWake = Actions("WAKE_WORD_FILE")
            actionWake.Activate()

        if actionStop is None:
            actionStop = Actions("STOP_WORD_FILE")
            actionStop.Activate()

        if answerRecorder is None:
            answerRecorder = Recorder()

        if voice is None:
            voice = TextToSpeech()

        count += 1
        sleep(0.01)

        if answerRecorder.IsRecording():
            answerRecorder.StopRecording()

        else:

            userRecordedInput = answerRecorder.HasRecording()
            transcriptRawSize = len(userRecordedInput)
            # print("Iter: ", count, " Idle")

            if transcriptRawSize > 0:

                response = None
                try:
                    print("Iter: ", count, " has Recording Size: ", transcriptRawSize)

                    transcript, words = leopardClient.process(userRecordedInput)
                    print("Has Transcript ", transcript)

                    if len(transcript) > 0:

                        response = chatGPT.Query(transcript)
                        chatGPT.AppendAnswer(response)
                        
                    
                except openai.error.APIError as e:
                    response = (
                        "\nThere was an API error.  Please try again in a few minutes."
                    )
                except openai.error.Timeout as e:
                    response = (
                        "\nYour request timed out.  Please try again in a few minutes."
                    )
                except openai.error.RateLimitError as e:
                    response = "\nYou have hit your assigned rate limit."
                except openai.error.APIConnectionError as e:
                    response = "\nI am having trouble connecting to the API.  Please check your network connection and then try again."
                except openai.error.AuthenticationError as e:
                    response = "\nYour OpenAI API key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program."
                except openai.error.ServiceUnavailableError as e:
                    response = "\nThere is an issue with OpenAI's servers.  Please try again later."

                answerRecorder.CleanRecording()
                
                if response is not None:
                    print("\nMerlin response is:\n")
                    voice.Tell(response)
                    txtDisplay = TextDisplay()
                    txtDisplay.Tell(response)

            else:

                if actionWake.IsActivated():

                    if firstTime:
                        firstTime = False
                        voice2 = TextToSpeech()
                        voice2.Tell("I'm here")
                        sleep(1)

                    if answerRecorder.IsNew():
                        answerRecorder.StartRecording()
                        listen()
                        detect_silence()
                    else:
                        if voice.Finished():
                            print("Voice Finished!")
                            voice = None
                            answerRecorder = None

                if actionStop.IsActivated():
                    voice2 = TextToSpeech()
                    voice2.Tell("Ok, I'll stop!")
                    actionStop = None
                    actionWake = None
                    firstTime = True
                    answerRecorder = None


except KeyboardInterrupt:
    print("\nExiting ChatGPT Virtual Assistant")
    leopardClient.delete
