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
        self._silenceAudioObj = pyaudio.PyAudio()
        self._listenAudioObj = pyaudio.PyAudio()

    def Listen(self, stopObject):

        self._stop = False
        self._invoked = False

        try:
            print("Listening...")

            listen_audio_stream = self._listenAudioObj.open(
                rate=self._cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._cobra.frame_length,
            )

            frameLength = self._cobra.frame_length

            while stopObject and stopObject.IsInvoked() is False:
                listen_pcm = listen_audio_stream.read(frameLength)
                listen_pcm = struct.unpack_from("h" * frameLength, listen_pcm)
                listenValue = self._cobra.process(listen_pcm)

                if listenValue > self._listenerThreshold:
                    print("\nVoice detected at [0-1] level:", listenValue)
                    listen_audio_stream.stop_stream()
                    listen_audio_stream.close()
                    # self._cobra.delete()
                    break
                else:
                    print(".", end="")

        except Exception as error:
            print("Error Listening:", error)

    def DetectSilence(self, stopObject):

        try:
            print("Detecting Silence...")

            cobra_audio_stream = self._silenceAudioObj.open(
                rate=self._cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._cobra.frame_length,
            )

            last_voice_time = time.time()
            frameLength = self._cobra.frame_length

            while stopObject and stopObject.IsInvoked() is False:
                cobra_pcm = cobra_audio_stream.read(frameLength)
                cobra_pcm = struct.unpack_from("h" * frameLength, cobra_pcm)

                silenceValue = self._cobra.process(cobra_pcm)
                if silenceValue > self._silenceThreshold:
                    print("_", end="")
                    last_voice_time = time.time()
                else:
                    silence_duration = time.time() - last_voice_time

                    if silence_duration > self._silenceDuration:
                        print("\nTotal Silence of: ", silence_duration, " seconds")
                        cobra_audio_stream.stop_stream()
                        cobra_audio_stream.close()
                        # self._cobra.delete()
                        last_voice_time = None
                        break

        except Exception as error:
            print("Error Detecting Silence:", error)

        self._stop = True
        self._invoked = True

        return True
