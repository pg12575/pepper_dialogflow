from naoqi import ALBroker
import threading
from pepper_recorder import SoundProcessingModule

if __name__ == '__main__':
    IP = "192.168.0.120" #Change this to your Pepper's IP address

    # Creation of a new Python Broker
    stop_recognition = threading.Event()
    pythonBroker = ALBroker("pythonBroker","0.0.0.0",9999, IP, 9559)
    print("connected")

    ## Need to find commands that will disable Pepper's blue eyes and default chatbot while the script is running.
    #asr = ALProxy("ALSpeechRecognition", self.ip, 9559)
    #asr.setVisualExpression(False)
    MySoundProcessingModule = SoundProcessingModule("MySoundProcessingModule", IP, stop_recognition)

    MySoundProcessingModule.startProcessing()
    pythonBroker.shutdown()
    print("disconnected")
