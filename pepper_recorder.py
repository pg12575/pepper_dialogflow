import StringIO
from Queue import Queue
from naoqi import ALModule, ALProxy
import numpy as np
import time
import logging
import uuid
import traceback
import wave
import pyaudio
from subprocess import call

LISTEN_RETRIES = 20 # How long to wait after silence before stopping audio recording. Smaller value breaks audio into smaller recordings.
DIALOG_FLOW_GCP_PROJECT_ID = "jokes-fvvqts" # Your dialogflow Project ID

class SoundProcessingModule(ALModule):
    def __init__( self, name, ip, stop_recognition):
        try:
            ALModule.__init__( self, name );
        except Exception as e:
            logging.error(str(e))
            pass
        print("connected")
        self.ip = ip
        self.BIND_PYTHON( name, "processRemote")
        self.ALAudioDevice = ALProxy("ALAudioDevice", self.ip, 9559)

        self.framesCount=0
        self.count = LISTEN_RETRIES
        self.recordingInProgress = False
        self.stopRecognition = stop_recognition
        self.uuid = uuid.uuid4()
        self.previous_sound_data = None

    def startProcessing(self):
        """init sound processing, set microphone and stream rate"""
        print("startProcessing")
        self.ALAudioDevice.setClientPreferences(self.getName(), 16000, 4, 0)
        self.ALAudioDevice.subscribe(self.getName())
        while not self.stopRecognition.is_set():
            time.sleep(1)

        self.ALAudioDevice.unsubscribe(self.getName())

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):

        """audio stream callback method with simple silence detection"""
        self.framesCount = self.framesCount + 1
        sound_data_interlaced = np.fromstring(str(inputBuffer), dtype=np.int16)
        sound_data = np.reshape(sound_data_interlaced, (nbOfChannels, nbOfSamplesByChannel), 'F')
        peak_value = np.max(sound_data)
        # detect sound
        if peak_value > 9000:
            #print("Peak:", peak_value)
            #time.sleep(0.5)
            self.count = LISTEN_RETRIES
            if not self.recordingInProgress:
                self.startRecording(self.previous_sound_data)

        # if there is no sound for a few seconds we end the current recording and start audio processing
        if self.count <= 0 and self.recordingInProgress:

            self.stopRecording()
        # if recording is in progress we save the sound to an in-memory file
        if self.recordingInProgress:
            self.count -= 1
            self.previous_data = sound_data
            self.procssingQueue.put(sound_data[0].tostring())
            self.outfile.write(sound_data[0].tostring())



    def startRecording(self, previous_sound_data):
        """init a in memory file object and save the last raw sound buffer to it."""
        self.outfile = StringIO.StringIO()
        self.procssingQueue = Queue()
        self.recordingInProgress = True
        if not previous_sound_data is None:
            self.procssingQueue.put(previous_sound_data[0].tostring())
            self.outfile.write(previous_sound_data[0].tostring())


        print("start recording")

    def stopRecording(self):
        """saves the recording to memory"""
        print("stopped recording")
        self.previous_sound_data = None
        self.outfile.seek(0)
        #print(self.outfile)
        frames = []
        CHUNK = 4096


        try:
            #detect_intent_stream(DIALOG_FLOW_GCP_PROJECT_ID, self.uuid, self.outfile, "en-US", self.ip)
            #print 'detect intent stream'
            while True:
                data = self.outfile.read(CHUNK)
                if not data:
                    break
                frames.append(data)
            #p = wave.open(self.outfile, 'r')


            wf = wave.open("output/file1.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)#self.outfile.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()
            exit_code = call("source venv/bin/activate; python3 chatbotlive.py", shell=True)
            #print(exit_code)
        except:
            traceback.print_exc()
        self.recordingInProgress = False
