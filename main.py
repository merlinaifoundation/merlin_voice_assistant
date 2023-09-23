import sys
import os
import wave
import pyaudio
import whisper
import openai
import time
import threading
import datetime
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
import simpleaudio as sa

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

openai.api_key = "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"

history = [
    {"role": "system", "content": "You are Merlin the Wizard, a helpful assistant."},
]

class Recorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Voice Note Recorder')
        self.setWindowIcon(QIcon('icon.png'))

        self.button = QPushButton('Record', self)
        self.button.setGeometry(75, 100, 150, 100)
        self.button.clicked.connect(self.on_button_click)

        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.recording = False
        self.rate = 44100
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1

    def on_button_click(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.audio = pyaudio.PyAudio()
        self.recording = True
        self.button.setText('Stop')
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        self.frames = []

        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            QCoreApplication.processEvents()

    def stop_recording(self):
        self.recording = False
        self.button.setText('Record')
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        filename = 'recorded_audio.wav'
        if os.path.exists(filename):
            os.remove(filename)

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)

        frames_copy = self.frames[:]
        wf.writeframes(b''.join(frames_copy))
        wf.close()

        self.frames = []

        model = whisper.load_model("base")
        result = model.transcribe(filename)
        print(result["text"])
        os.remove(filename)        

        def get_current_time():
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")

        global history
        question = result["text"]
        history.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            functions=[{
                "name": "get_current_time",
                "description": "Gets the current time",
                "result_type": {"type": "string"},
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }]
        )

        assistant_response = response.choices[0].message['content']
        if response.choices[0].message.get('function_call'):
            function_name = response.choices[0].message['function_call']['name']
            if function_name == 'get_current_time':
                # call your actual get_current_time function here
                assistant_response = get_current_time()

        history.append({"role": "assistant", "content": assistant_response})

        print(assistant_response)

        tts = gTTS(text=assistant_response, lang='en')
        tts.save("speech.mp3")
        audio_segment = AudioSegment.from_mp3("speech.mp3")
        playback = sa.play_buffer(audio_segment.raw_data, num_channels=audio_segment.channels, bytes_per_sample=audio_segment.sample_width, sample_rate=audio_segment.frame_rate)
        playback.wait_done()
        os.remove("speech.mp3")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Recorder()
    ex.show()
    sys.exit(app.exec_())
