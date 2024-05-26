from threading import Thread
import time
from decouple import config
import struct
import pyaudio
import pvcobra


class Listener(Thread):

    def __init__(self, listenThreshold=0.3, silenceDuration=1.3, _silenceThreshold=0.2):
        super().__init__()
        self._stop = True
        self._invoked = False
        pv_access_key = str(config("PV_ACCESS_KEY"))
        # print("Using PV KEY", pv_access_key)
        self._listenerThreshold = listenThreshold
        self._silenceDuration = silenceDuration
        self._silenceThreshold = _silenceThreshold
        self._cobra = pvcobra.create(access_key=pv_access_key)

    def Trigger(self):

        self.Listen()
        self.DetectSilence()

        self._stop = True
        self._invoked = True

    def Listen(self):

        try:
            print("Listening...")
            listen_pa = pyaudio.PyAudio()

            listen_audio_stream = listen_pa.open(
                rate=self._cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._cobra.frame_length,
            )

            while True:
                frameLength = self._cobra.frame_length
                listen_pcm = listen_audio_stream.read(frameLength)
                listen_pcm = struct.unpack_from("h" * frameLength, listen_pcm)

                if self._cobra.process(listen_pcm) > self._listenerThreshold:
                    print("Voice detected")
                    listen_audio_stream.stop_stream()
                    listen_audio_stream.close()
                    # self._cobra.delete()
                    break

        except Exception as error:
            print("Error:", error)

    def DetectSilence(self):

        try:
            print("Detect Silence")
            silence_pa = pyaudio.PyAudio()

            cobra_audio_stream = silence_pa.open(
                rate=self._cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._cobra.frame_length,
            )

            last_voice_time = time.time()

            while True:
                frameLength = self._cobra.frame_length
                cobra_pcm = cobra_audio_stream.read(frameLength)
                cobra_pcm = struct.unpack_from("h" * frameLength, cobra_pcm)

                if self._cobra.process(cobra_pcm) > self._silenceThreshold:
                    last_voice_time = time.time()
                else:
                    silence_duration = time.time() - last_voice_time
                    if silence_duration > self._silenceDuration:
                        print("Text interpreted\n")
                        cobra_audio_stream.stop_stream()
                        cobra_audio_stream.close()
                        # self._cobra.delete()
                        last_voice_time = None
                        break

        except Exception as error:
            print("Error:", error)
