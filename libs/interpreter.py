from threading import Thread
from decouple import config
import pvleopard

from openai import OpenAI
import os

import wave


class Interpreter(Thread):

    def __init__(self):
        super().__init__()

        pv_access_key = str(config("PV_ACCESS_KEY"))
        # print("Using PV KEY", pv_access_key)

        self.leopardClient = pvleopard.create(
            access_key=pv_access_key,
            enable_automatic_punctuation=True,
        )
        self.client = OpenAI()

    def bytes_to_wav(self, byte_data, filename):
        with wave.open(filename, "wb") as wav_file:

            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # 16-bit samples
            wav_file.setframerate(16000)  # Sample rate (e.g., 44.1 kHz)
            wav_file.writeframes(byte_data)

        # Example usage:
        # audio_bytes = b'\x01\x02\x03...'  # Replace with your actual audio data
        # bytes_to_wav(audio_bytes, 'output.wav')

    def SpeechToTextOpenAI(self, userRecordedInput):
        # print(userRecordedInput)
        #bytes_object = bytes([i % 256 for i in userRecordedInput])
        #self.bytes_to_wav(bytes_object, "PRUEBA.mp3")

        audio_file = open("PRUEBA.mp3", "rb")
        # audio_file = open("test.m4a", "rb")

        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )

        return transcription

        transcript = ""
        transcriptRawSize = len(userRecordedInput)

        if transcriptRawSize > 0:
            print("Has Recording Size: ", transcriptRawSize)
            temp_file_path = self.buffer_to_temp_file(userRecordedInput)

            with open(temp_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="text"
                )
                transcript = response.text
                print("Transcript: ", transcript)

            # Clean up the temporary file
            os.remove(temp_file_path)

        return transcript

    def SpeechToText(self, userRecordedInput):
        transcript = ""
        words = []
        transcriptRawSize = len(userRecordedInput)
        # print("Interpreting")
        if transcriptRawSize > 0:
            print("Has Recording Size: ", transcriptRawSize)
            transcript, words = self.leopardClient.process(userRecordedInput)
            print("Transcript: ", transcript, len(words))

        return transcript
