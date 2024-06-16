import os
import random
from threading import Thread
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
        self._bufferLimit = bufferLimit or int(cfgLimit) or 1e7
        self._finalized = False
        self.p = pyaudio.PyAudio()
        print(
            "Recording Buffer Limit set at: ",
            self._bufferLimit,
            self.p.get_sample_size(FORMATO),
        )

        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self.file_path = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )

    def run(self):
        # start recording
        # self._recorder.start()
        print("Recording...", self.file_path)

        flujo = self.p.open(
            format=FORMATO,
            channels=CANALES,
            rate=TASA_MUESTREO,
            input=True,
            frames_per_buffer=CHUNK,
        )

        while self._is_recording:
            # read

            # Abrir el flujo de grabación

            # print("Grabando...")

            # Grabar los datos en fragmentos y añadir al arreglo de frames
            # for i in range(0, int(TASA_MUESTREO / CHUNK * DURACION)):
            # datos = flujo.read(CHUNK)
            # frames.append(datos)

            # print("Grabación terminada.")

            # Detener y cerrar el flujo de grabación
            reading = flujo.read(CHUNK)

            # if more data than limit, clean buffer
            if len(self._buffer) > self._bufferLimit:
                print(
                    "\nRecorder Buffer Limit was Hit",
                    len(self._buffer),
                    ". Flushing...",
                    self.file_path,
                )
                self._buffer = []
            # append to buffer
            if len(reading) > 0:
                self._buffer.append(reading)
        # stop recording
        self._result = self._buffer.copy()
        flujo.stop_stream()
        flujo.close()
        self.p.terminate()

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

    def HasRecordingObj(self):
        return self._result

    def RemoveRecording(self):
        try:
            # os.remove(self.file_path)
            print("Removing Recording: ", self.file_path)
            # os.remove(self.file_path)

        except Exception as error:
            print("Error Removing Recording", error)

    def CleanRecording(self):
        self._result = []
        self._buffer = []

    def StopRecording(self):
        self._is_recording = False
        while not self._stop:
            # print('.', end='')
            pass

    def SaveRecordingObj(self):
        if len(self._result) > 0:
            # Convert the buffer to a numpy array
            wf = wave.open(self.file_path, "wb")
            wf.setnchannels(CANALES)
            wf.setsampwidth(self.p.get_sample_size(FORMATO))
            wf.setframerate(TASA_MUESTREO)
            wf.writeframes(b"".join(self._result))
            wf.close()
            # audio_segment.export(self.file_path, format="mp3")
            print(f"Recording saved to {self.file_path}")

            # audio_segment = None
            return self.file_path
