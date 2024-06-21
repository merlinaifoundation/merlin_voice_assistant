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
        self._is_recording = True

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

        self._assignFileName()
        self._cummulative = []
        self._stream = None
        self._stop = False
        self._discardLast = False

    def _assignFileName(self):
        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self._output_file = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )

    def _openStream(self):

        if self._stream is None:
            print("Recording...", self._output_file)

            self._buffer = []

            self._stream = self._pyAudio.open(
                format=FORMATO,
                channels=CANALES,
                rate=TASA_MUESTREO,
                input=True,
                frames_per_buffer=CHUNK,
            )

    def _closeStream(self):
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

    def TrimLeftRecording(self):
        # DETECT WHEN VOICE ACTIVATES AND STORE RECORDING FROM THERE - BIAS (cut length)
        stored = self.GetBufferObj()
        getIndex = len(stored)

        if getIndex > self._cutLength:
            print("Cutting at index =", getIndex)
            stored = stored[getIndex - self._cutLength : getIndex]
            self.SetBufferObj(stored)

    def StartThread(self):
        self.start()

    def StopThread(self):
        self._stop = True

    def _buffering(self):

        # read
        if self._stream:
            reading = self._stream.read(CHUNK)
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

    def run(self):

        while not self._stop:

            time.sleep(0.001)

            try:
                while self._is_recording:

                    time.sleep(0.001)
                    self._buffering()

                self._closeStream()

            except Exception as error:
                print("Error in Recorder", error)

            if not self._finalized: 
                if not self._discardLast:
                    aux = self._buffer.copy()
                    if len(aux):
                        self._cummulative.append(aux.copy())
                self._discardLast = False
                self._finalized = True

        self._pyAudio.terminate()

    def StartRecording(self):
        if not self._is_recording and self._finalized:
            
            self._buffer = []
            
            self._finalized = False
            
            self._openStream()
            
            self._is_recording = True
            # self._buffer = []

    def IsRecording(self):
        return self._is_recording

    # def Finished(self):
    # return  self._finalized

    def GetBufferObj(self):
        return self._buffer

    def SetBufferObj(self, obj):
        self._buffer = obj

    def GetRecordingObj(self):

        if len(self._cummulative) > 0:
            return self._cummulative.pop(0)
        return []

    def RemoveRecording(self):
        try:
            if os.path.isfile(self._output_file):
                os.remove(self._output_file)
                print("Removing Recording: ", self._output_file)

        except Exception as error:
            print("Error Removing Recording", error)

    def StopRecording(self, discard_result = False):
        #set flag
        self._discardLast = discard_result
        #stop process
        self._is_recording = False

    def SaveRecordingObj(self, obj):
        try:
            if len(obj) > 0:
                self._assignFileName()
                # Convert the buffer to a numpy array
                wf = wave.open(self._output_file, "wb")
                wf.setnchannels(CANALES)
                wf.setsampwidth(self._pyAudio.get_sample_size(FORMATO))
                wf.setframerate(TASA_MUESTREO)
                wf.writeframes(b"".join(obj))
                wf.close()
                # audio_segment.export(self.file_path, format="mp3")
                print(f"Recording saved to {self._output_file}")
                # audio_segment = None
                return self._output_file

        except Exception as error:
            print("Error Saving Recording: ", error)

        return None
