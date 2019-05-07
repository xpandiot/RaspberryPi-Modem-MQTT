#install paho mqtt library for python before using the code. You can find that library inside the zip file.  

import paho.mqtt.client as mqttClient
import time
import RPi.GPIO as GPIO
import json
import subprocess
import io

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Please change the device serial according to the serial key given by the consumer portal

DEVICE_SERIAL = "9689849699110176" //update your device serial number as per Device operation from the IOT Platfrom

#topics for sending events and receiving action messages . Change the SUB TOPIC based on device onboarding
SUBSCRIBED_TOPIC = "+/" + DEVICE_SERIAL + "/generic_brand_392/generic_device/piv1/sub" 

EVENT_TOPIC = "generic_brand_392/generic_device/piv1/common"

connected = 0



def connect(tries):
    global client
    global connected
    if tries < 1:
	connected = 0
        return

    try:
		client.connect(broker_address, port, KEEPALIVE)
		print("Connected to " + broker_address + " : " + port)
		connected = 1
		return

    except:
        print("Can't connect to the server")
        time.sleep(5)
        tries = tries - 1
        connect(tries)
		
		
def on_connect(client, userdata, flags, rc):
    print "Subscribing to topic " + SUBSCRIBED_TOPIC
    client.subscribe(SUBSCRIBED_TOPIC)
    #subprocess.call(['./test.sh']) 
 
def on_message(client, userdata, message):
	print "Message received: "  + message.payload
	# print "msg testing."
	do_actions(message.payload)
	#send_events()
	
def publish_message(message):
	client.publish(EVENT_TOPIC,message,0,False)

	
#====================================================================================================================================================================	
def send_events():
	#create this function to send some events to the backend. You should create a message format like this
	"""Eg :{
				"mac":"6655591876092787",
				"eventName":"eventOne",
				"state":"none",
				"eventOne":{
					"ev1Value1":30
				}
			}
	
	"""
	#Should call this function to send events. Pass your message as parameter
	f = open("/sys/class/thermal/thermal_zone0/temp", "r")
	t = float(f.readline ())/1000
	cpuTemp = str(t)
	print "CPU temp: " + cpuTemp
	message = "{\"eventName\":\"dataChanged\",\"status\":\"none\",\"event\":{\"proctemp\":"+ cpuTemp +"},\"mac\":\""+ DEVICE_SERIAL +"\"}"
	#message = "{\"mac\":\"6655591876092787\",\"eventName\":\"eventOne\",\"state\":\"none\",\"eventOne\":{\"ev1Value1\":30}}"
	print "message published successfully"
	publish_message(message)

#====================================================================================================================================================================
#====================================================================================================================================================================	
def do_actions(message):


        msg=json.loads(message)
        action = msg["action"]
        # pin=int(msg["param"]["ac1Value4"])
        #action=msg["param"]["period"]
	
	gpioPin = 16

        print "action passed."
        
        for x in range(10):

            if action=="on":
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(gpioPin,GPIO.OUT,initial=GPIO.HIGH)
                    GPIO.output(gpioPin,1)
                    
                    time.sleep(0.5)

                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(gpioPin,GPIO.OUT,initial=GPIO.LOW)
                    GPIO.output(gpioPin,0)

                    time.sleep(0.5)
		
        #     print action
        #     print port
        # elif action == "off":
        #     GPIO.setmode(GPIO.BCM)
        #     GPIO.setup(port,GPIO.OUT,initial=GPIO.LOW)
        #     GPIO.output(port,0)
        #     print action
        #     print port
        # else:
        #     print "invalid action"

	#Create this function according to your actions. you will receive a message something like this

#=====================================================================================================================================================================	
#Connected = False   #global variable for the state of the connection
 
broker_address= "mqtt.iot.ideamart.io"  #Broker address
# broker_address= "52.224.154.229"  #Broker address
port = "1883"                         #Broker port
user = "generic_brand_392-generic_device-piv1_2112"                    #Connection username
password = "1556516066_2112"            #Connection password
KEEPALIVE = 6;
 
client = mqttClient.Client(DEVICE_SERIAL)               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
#client.on_publish= send_events

while 1:
	global connected

	if connected==0:
    		connect(5)
    	send_events()
    	#client.loop_start()
    	#send_events()
    	# TODO : Update to use a keyboard interrupt
    	time.sleep(10)
    	#client.loop_stop()
    	#client.disconnect()
