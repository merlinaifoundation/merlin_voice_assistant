import os
from threading import Thread
import struct
import time
import pvporcupine
import pyaudio


class Action(Thread):

    def __init__(self, pv_access_key, wakeWordFile, channels , frame_length, rate):
        super().__init__()
        self.name = 'Action' + str(wakeWordFile)
        self._wake_pa = pyaudio.PyAudio()
        default_input_device = self._wake_pa.get_default_input_device_info()
        print(f"Default Input Device: {default_input_device['name']}")
        
        self._is_stopped = True
        self._invoked = False
        self.wakeWordFile = wakeWordFile
        rootPath = os.path.dirname(__file__)
        self._keyword_path = os.path.join(rootPath, self.wakeWordFile)
        self._apiKey = str(pv_access_key)
        self._stopThread = False
        self.porcupineStream = None
        self._createClient( channels, frame_length, rate)
        #self._openStream()
        print("\nWakeWord Routine from: ", self.wakeWordFile)
        

    def _createClient(self,  channels,  frame_length, rate):
        self.porcupineClient = pvporcupine.create(
            access_key=self._apiKey, keyword_paths=[self._keyword_path]
        )
        self._channels = channels or 1
        self.frame_length = frame_length  or self.porcupineClient.frame_length
        self.rate = rate or self.porcupineClient.sample_rate
        print("Actions params at: ", (self._channels, self.frame_length, self.rate)) #  (1, 512, 16000) or defaults
        
        

    def _openStream(self):
        
        if self.porcupineStream is None:
            self.porcupineStream = self._wake_pa.open(
                rate=self.rate ,
                channels=self._channels , # does not work stereo
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.frame_length
                
            )
        

    def StartThread(self):
        self.start()
    def StopThread(self):
        self._stopThread = True
    def StartListening(self):
        print("Restarting Listen Action")
        if not self._invoked:
            self._is_stopped = False
        
        
            
            
    def StopListening(self):
        print("Stoping Listen Action...")
        self._is_stopped = True
        self._invoked = False
        

    def IsInvoked(self):
        return self._invoked

    def SetInvoked(self, finalized):
        self._invoked = finalized
        if finalized:
            self._is_stopped = True

    def run(self):

        while not self._stopThread :
            
            time.sleep(0.001)
            try:

                
                
                
                while not self._is_stopped:
                    
                    self._openStream()
                    
                    time.sleep(0.001)
                    
                    if self.porcupineStream:
                        
                        frameLength = self.frame_length or self.porcupineClient.frame_length
                        porcupine_pcm = self.porcupineStream.read(frameLength)
                        porcupine_pcm = struct.unpack_from("h" * frameLength, porcupine_pcm)
                        porcupine_keyword_index = self.porcupineClient.process(porcupine_pcm)

                        if porcupine_keyword_index >= 0:

                            self.SetInvoked(True)
                            print("\nAction Phrase Detected as in file: ", self.wakeWordFile)


                try:
                    
                    if self.porcupineStream:       
                        self.porcupineStream.stop_stream()
                        self.porcupineStream.close()
                        self.porcupineStream = None
                    
                except Exception as error:
                    print("\nError Closing Wake Stream", error, self.wakeWordFile)
                    break
                                
            
            except Exception as error:
                print("\nError Opening Wake Stream", error,  self.wakeWordFile)
                break

            
        
        
        try:
        
            self.porcupineClient.delete()
            self._wake_pa.terminate()
            
        except Exception as error:
            print("\nError Terminating Wake Clients", error, self.wakeWordFile)
        