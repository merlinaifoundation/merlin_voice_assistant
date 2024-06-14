import os
import random
from threading import Thread
from pvrecorder import PvRecorder
from decouple import config
from pydub import AudioSegment
import numpy as np


class Recorder(Thread):
    def __init__(self, bufferLimit=None):
        super().__init__()
        self._buffer = []
        self._result = []
        self._is_recording = False
        self._stop = True

        cfgLimit = config("REC_BUFFER_LIMIT")
        self._bufferLimit = bufferLimit or int(cfgLimit) or 1e7
        print("Recording Buffer Limit set at: ", self._bufferLimit)
        self._finalized = False
        self._recorder = PvRecorder(device_index=-1, frame_length=512)
        rootPath = os.path.dirname(__file__)
        internalPath = str(random.randint(0, 1000000)) + ".mp3"
        self.file_path = os.path.join(
            rootPath,
            "tmp",
            internalPath,
        )

    def run(self):
        # start recording
        self._recorder.start()
        print("Recording...", self.file_path)
        while self._is_recording:
            # read
            reading = self._recorder.read()
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
                self._buffer.extend(reading)
        # stop recording
        self._recorder.stop()
        self._recorder.delete()
        # append result to final variable
        self._result = self._buffer.copy()

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
            os.remove(self.file_path)

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
            audio_data = np.array(self._result, dtype=np.int16)

            # Create an AudioSegment from the numpy array
            audio_segment = AudioSegment(
                audio_data.tobytes(),
                frame_rate=self._recorder.sample_rate,
                sample_width=audio_data.dtype.itemsize,
                channels=1,
            )

            # Export the AudioSegment to an MP3 file
            audio_segment.export(self.file_path, format="mp3")
            print(f"Recording saved to {self.file_path}")

            audio_segment = None
            return self.file_path
