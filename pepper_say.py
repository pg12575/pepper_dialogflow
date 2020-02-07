from naoqi import ALProxy

with open ("output/response.txt", "r") as myfile:
    data=myfile.readlines()
tts = ALProxy("ALAnimatedSpeech", "192.168.0.120", 9559)
tts.say("\\rspd=90\\" + str(data))
