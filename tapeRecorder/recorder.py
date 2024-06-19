import os
import random
from threading import Thread
import time
from decouple import config

import pyaudio
import wave

# Definir los parámetros de la grabación
FORMATO = pyaudio.paInt16
CANALES = 2
TASA_MUESTREO = 44100
CHUNK = 1024
DURACION = 5

# Inicializar PyAudio


class Recorder(Thread):
    def __init__(self, bufferLimit=None):
        super().__init__()
        self._buffer = []
        self._result = []
        self._is_recording = False
        self._stop = True

        cfgLimit = config("REC_BUFFER_LIMIT")
        self._cutLength = int(config("LISTEN_LENGTH"))

        self._bufferLimit = bufferLimit or int(cfgLimit) or 1e7
        self._finalized = False
        self._pyAudio = pyaudio.PyAudio()
        print(
            "Recording Buffer Limit set at: ",
            self._bufferLimit,
            self._pyAudio.get_sample_size(FORMATO),
        )

        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self._output_file = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )

    def TrimLeftRecording(self):
        # DETECT WHEN VOICE ACTIVATES AND STORE RECORDING FROM THERE - BIAS (cut length)
        stored = self.GetBufferObj()
        getIndex = len(stored)
        
        if getIndex >  self._cutLength:
            print("Cutting at index =", getIndex)
            stored = stored[getIndex - self._cutLength : getIndex]
            self.SetBufferObj(stored)

    def run(self):
        # start recording
        # self._recorder.start()
        print("Recording...", self._output_file)

        flujo = self._pyAudio.open(
            format=FORMATO,
            channels=CANALES,
            rate=TASA_MUESTREO,
            input=True,
            frames_per_buffer=CHUNK,
        )

        while self._is_recording:
            time.sleep(0.01)

            # read

            reading = flujo.read(CHUNK)

            # if more data than limit, clean buffer
            if len(self._buffer) > self._bufferLimit:
                print(
                    "\nRecorder Buffer Limit was Hit",
                    len(self._buffer),
                    ". Flushing...",
                    self._output_file,
                )
                self._buffer = []
            # append to buffer
            if len(reading) > 0:
                self._buffer.append(reading)
        # stop recording
        self._result = self._buffer.copy()
        
        flujo.stop_stream()
        flujo.close()
        self._pyAudio.terminate()

        # flags
        self._stop = True
        # self._is_recording = False
        self._finalized = True

    def StartRecording(self):
        if self._stop and self._finalized is False:
            self._stop = False
            self._is_recording = True
            self.start()

    def IsRecording(self):

        return self._is_recording

    def Finished(self):
        return self._finalized

    def GetBufferObj(self):
        return self._buffer

    def GetRecordingObj(self):
        return self._result

    def SetBufferObj(self, obj):
        self._buffer = obj

    def RemoveRecording(self):
        try:
            if os.path.isfile(self._output_file):
                os.remove(self._output_file)
                print("Removing Recording: ", self._output_file)

        except Exception as error:
            print("Error Removing Recording", error)

    def CleanRecording(self):
        self._result = []
        self._buffer = []

    def StopRecording(self):
        self._is_recording = False
        while not self._stop:
            time.sleep(0.001)
            # print('.', end='')
            pass

    def SaveRecordingObj(self):
        try:
            if len(self._result) > 0:
                # Convert the buffer to a numpy array
                wf = wave.open(self._output_file, "wb")
                wf.setnchannels(CANALES)
                wf.setsampwidth(self._pyAudio.get_sample_size(FORMATO))
                wf.setframerate(TASA_MUESTREO)
                wf.writeframes(b"".join(self._result))
                wf.close()
                # audio_segment.export(self.file_path, format="mp3")
                print(f"Recording saved to {self._output_file}")
                # audio_segment = None
                return self._output_file
        
        except Exception as error:
            print("Error Saving Recording: ",error)
        
        return None
