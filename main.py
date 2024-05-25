import os
import struct
import sys
import threading
import time
from time import sleep
from decouple import config
from colorama import Fore
import random

import openai

import pvcobra
import pvporcupine
import pyaudio

import pvleopard

#NEW LIBS
from textResponder import TextDisplay
from textToSpeech import TextToSpeech
from recorder import Recorder
from gpt import ChatGPT

audio_stream = None
pa = None
wav_file = None

pv_access_key = config("PV_ACCESS_KEY")
wakeWord = config("WAKE_WORD_FILE")

print("Using PV KEY", pv_access_key)
print("Using WAKE WORD", wakeWord)

chatGPT = ChatGPT()




def append_clear_countdown():
    sleep(300)

    chatGPT.ClearCummulativeAnswers()
    chatGPT.SwitchModel()

    global count
    count = 0
    t_count.join


def wake_word():
    rootPath = os.path.dirname(__file__)
    keyword_path = os.path.join(rootPath, wakeWord)
    
    porcupine = pvporcupine.create(
        access_key=pv_access_key, keyword_paths=[keyword_path]
    )
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

    wake_pa = pyaudio.PyAudio()

    porcupine_audio_stream = wake_pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    Detect = True

    while Detect:
        porcupine_pcm = porcupine_audio_stream.read(porcupine.frame_length)
        porcupine_pcm = struct.unpack_from("h" * porcupine.frame_length, porcupine_pcm)

        porcupine_keyword_index = porcupine.process(porcupine_pcm)

        if porcupine_keyword_index >= 0:
            print(Fore.GREEN + "\nWake word detected\n")
            porcupine_audio_stream.stop_stream
            porcupine_audio_stream.close()
            porcupine.delete()
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            Detect = False


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

    event = threading.Event()
    count = 0

    while True:

        answerRecorder = Recorder()
        voice = TextToSpeech()
        txtDisplay = TextDisplay()

        try:

            if count == 0:
                t_count = threading.Thread(target=append_clear_countdown)
                t_count.start()
            else:
                pass
            count += 1

            wake_word()

            # voice.Tell(random.choice(chatGPT.prompt))

            answerRecorder.StartRecording()

            listen()

            detect_silence()

            userRecordedInput = answerRecorder.StopRecording()

            transcript, words = leopardClient.process(userRecordedInput)

            print(transcript)

            response = chatGPT.Query(transcript)
            chatGPT.AppendAnswer(response)

        except openai.error.APIError as e:
            response = "\nThere was an API error.  Please try again in a few minutes."
        except openai.error.Timeout as e:
            response = "\nYour request timed out.  Please try again in a few minutes."
        except openai.error.RateLimitError as e:
            response = "\nYou have hit your assigned rate limit."
        except openai.error.APIConnectionError as e:
            response = "\nI am having trouble connecting to the API.  Please check your network connection and then try again."
        except openai.error.AuthenticationError as e:
            response = "\nYour OpenAI API key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program."
            break
        except openai.error.ServiceUnavailableError as e:
            response = (
                "\nThere is an issue with OpenAI's servers.  Please try again later."
            )

        answerRecorder.StopRecording()
        event.set()
        print("\nMerlin response is:\n")

        voice.Tell(response)
        txtDisplay.Tell(response)
        sleep(1)
        
        

except KeyboardInterrupt:
    print("\nExiting ChatGPT Virtual Assistant")
    leopardClient.delete
