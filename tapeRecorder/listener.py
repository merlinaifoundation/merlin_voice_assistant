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

        self._averageListenerThreshold = []
        self._averageSilenceDuration = []
        self._averageSilenceThreshold = []
        self.iterator = 0
        self._cancelled = False

    def SetCancelled(self, cancelled):
        self._cancelled = cancelled
    def Listen(self):

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

            while self._cancelled is False:
                listen_pcm = listen_audio_stream.read(frameLength)
                listen_pcm = struct.unpack_from("h" * frameLength, listen_pcm)
                listenValue = self._cobra.process(listen_pcm)

                
                self._averageListenerThreshold.append( listenValue)
                
                lenghtOfArray = len(self._averageListenerThreshold)
                
                if lenghtOfArray > 10:
                    self._averageListenerThreshold.pop(0)
                
                if listenValue > self._listenerThreshold:
                    
                    if lenghtOfArray > 10 :
                        suma = sum(self._averageListenerThreshold)
                        avg = round(suma / lenghtOfArray,2)
                        print ("\nAverage Listening Threshold: ", avg, lenghtOfArray, self._listenerThreshold )
                        #self._listenerThreshold = 5*avg
                        
                    print("\nVoice detected at [0-1] level:", round(listenValue), self._listenerThreshold)
                    # self._cobra.delete()
                    break
                else:
                    print(".", end="")
                
            listen_audio_stream.stop_stream()
            listen_audio_stream.close()

        except Exception as error:
            print("Error Listening:", error)

    def DetectSilence(self):

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

            while self._cancelled is False:
                cobra_pcm = cobra_audio_stream.read(frameLength)
                cobra_pcm = struct.unpack_from("h" * frameLength, cobra_pcm)

                silenceValue = self._cobra.process(cobra_pcm)
                
                self._averageSilenceThreshold.append( silenceValue)
                
                lenghtOfArray = len(self._averageSilenceThreshold)
                
                if lenghtOfArray > 10:
                    self._averageSilenceThreshold.pop(0)
                    
                if silenceValue > self._silenceThreshold:
                    print("_", end="")
                    last_voice_time = time.time()
                    
                else:
                    
                    silence_duration = time.time() - last_voice_time
                    
                    self._averageSilenceDuration.append( silence_duration)
                    if lenghtOfArray > 10:
                        self._averageSilenceDuration.pop(0)
                    
                    if silence_duration > self._silenceDuration:
                        
                        if lenghtOfArray > 10 :
                            suma = sum(self._averageSilenceDuration)
                            avg = round(suma / lenghtOfArray,2)
                            print ("\nAverage Silence Duration: ", avg, lenghtOfArray, self._silenceDuration )
                            #self._silenceDuration = 2*avg
                            
                            suma = sum(self._averageSilenceThreshold)
                            avg = round(suma / lenghtOfArray,2)
                            print ("\nAverage Silence Threshold: ", avg, lenghtOfArray, self._silenceThreshold )
                            #self._silenceThreshold = 5*avg
                        
                        print("\nTotal Silence of: ", round(silence_duration,2), " seconds")
                        # self._cobra.delete()
                        last_voice_time = None
                        break
            
            cobra_audio_stream.stop_stream()
            cobra_audio_stream.close()
            
        except Exception as error:
            print("Error Detecting Silence:", error)

        self._stop = True
        self._invoked = True

        return True
