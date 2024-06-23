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
        self.name = 'Recorder'

        self._buffer = []
        self._result = []
        self._isRecording = False

        REC_BUFFER_LIMIT = config("REC_BUFFER_LIMIT")
        self._LISTEN_LENGTH = int(config("LISTEN_LENGTH"))
        self._REC_BUFFER_LIMIT = bufferLimit or int(REC_BUFFER_LIMIT) or 1e7
        self._finalized = True
        self._pyAudioObj = pyaudio.PyAudio()
        print(
            "\nRecording Buffer Limit set at: ",
            self._REC_BUFFER_LIMIT,
            self._pyAudioObj.get_sample_size(FORMATO),
        )

        self._assignFileName()
        self._cummulativeBuffers = []
        self._audiostream = None
        self._stopThread = False
        self._discardLastBuffer = True

    def _assignFileName(self):
        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self._output_file = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )

    def _openStream(self):

        if self._audiostream is None:
            print("\nRecording...", self._output_file)

            self._audiostream = self._pyAudioObj.open(
                format=FORMATO,
                channels=CANALES,
                rate=TASA_MUESTREO,
                input=True,
                frames_per_buffer=CHUNK,
            )

    def _closeStream(self):
        if self._audiostream:
            self._audiostream.stop_stream()
            self._audiostream.close()
            self._audiostream = None

    def TrimLeftRecording(self):
        # DETECT WHEN VOICE ACTIVATES AND STORE RECORDING FROM THERE - BIAS (cut length)
        stored = self._buffer
        getIndex = len(stored)

        if getIndex > self._LISTEN_LENGTH:
            print("\nCutting at index =", getIndex)
            stored = stored[getIndex - self._LISTEN_LENGTH : getIndex]
            self._buffer = stored

    def StartThread(self):
        self.start()

    def StopThread(self):
        self._stopThread = True

    def _appendToList(self):
        if not self._finalized:
            if not self._discardLastBuffer:
                aux = self._buffer.copy()
                if len(aux):
                    self._cummulativeBuffers.append(aux)
                    self._discardLastBuffer = True
            self._buffer = []
            self._finalized = True

    def _buffering(self):

        # read
        if self._audiostream:
            reading = self._audiostream.read(CHUNK)
            # if more data than limit, clean buffer
            if len(self._buffer) > self._REC_BUFFER_LIMIT:
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

        while not self._stopThread:

            time.sleep(0.001)
            try:

                while self._isRecording:
                    time.sleep(0.001)
                    self._buffering()

                self._closeStream()
                self._appendToList()

            except Exception as error:
                print("\nError in Recorder", error)

        self._pyAudioObj.terminate()

    def StartRecording(self):
        # executes once
        if self._finalized:

            self._buffer = []
            self._finalized = False
            self._discardLastBuffer = False

            self._isRecording = True
            self._openStream()

    def IsRecording(self):
        return self._isRecording

    # def Finished(self):
    # return  self._finalized

    def TakeRecordingBuffer(self):

        if len(self._cummulativeBuffers) > 0:
            #return self._cummulativeBuffers.pop(0)
            flat_list = [x for sublist in self._cummulativeBuffers for x in sublist]
            self._cummulativeBuffers=[]
            return flat_list
        return []

    def DeleteRecordingFile(self, file):
        try:
            if file and os.path.isfile(file):
                os.remove(file)
                print("\nDeleting Recording: ", file)
                return True
        except Exception as error:
            print("\nError Deleting Recording", error)
        return False
    def StopRecording(self, discard_result=False):
        # set flag
        self._discardLastBuffer = discard_result
        # stop process
        self._isRecording = False

    def SaveRecordingFile(self, aBuffer):
        try:
            if aBuffer and len(aBuffer) > 0:
                self._assignFileName()
                # Convert the buffer to a numpy array
                wf = wave.open(self._output_file, "wb")
                wf.setnchannels(CANALES)
                wf.setsampwidth(self._pyAudioObj.get_sample_size(FORMATO))
                wf.setframerate(TASA_MUESTREO)
                wf.writeframes(b"".join(aBuffer))
                wf.close()
                # audio_segment.export(self.file_path, format="mp3")
                print(f"\nRecording saved to {self._output_file}")
                # audio_segment = None
                return self._output_file

        except Exception as error:
            print("\nError Saving Recording: ", error)

        return None
