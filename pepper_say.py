from naoqi import ALProxy
import time

with open ("output/response.txt", "r") as myfile:
    data=myfile.readlines()
tts = ALProxy("ALAnimatedSpeech", "192.168.0.120", 9559)
web = ALProxy("ALTabletService", "192.168.0.120", 9559)
print(str(data).split(' ', 1)[0])

#check if response starts with video
if str(data).split(' ', 1)[0] == "[\"video":
    data = str(data).split(' ', 1)[1]
    print(data)
    tts.say("\\rspd=90\\" + str(data))
    web.showWebview("https://www.youtube.com/results?search_query=funny+cat+videos")
elif str(data) == "[\'closevideo\']":
    web.hideWebview()
    tts.say("\\rspd=90\\Okay")

else:
    data = str(data)
    data1 = data[2:-2]
    #The line underneath can be used to show text on a webpage
    #web.showWebview("https://www.gzaas.com/preview/preview?gs_form="+ str(data1)+"&font=&color=&backColor=&pattern=&style=s_comic1&shadows=&visibility=1&from=preview" )
    tts.say("\\rspd=90\\" + str(data))
    #time.sleep(10)
    #web.hideWebview()
