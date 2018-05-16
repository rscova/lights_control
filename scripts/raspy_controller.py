#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

from std_msgs.msg import String
from lights_control.msg import LightingControl
from lights_control.srv import *

data = LightingControl(1111,'light',0)
data_string =  str(data.id) + " " + data.name + " "+str(data.state)

map_lights = {};
map_lights[0000] = {" ", 0}

GPIO.setmode(GPIO.BOARD)
OFF = 1
ON = 0

def releControl(data):
	rele = 0b11111 &  data.id - 2
	GPIO.output(rele, not(bool(data.state)))

	
def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8"))
    m_in = json.loads(m_decode)

    data.id = m_in["id"]
    data.name = str(m_in["name"])
    data.state = m_in["state"]

    rospy.loginfo("message received: %s", data)

    if map_lights.has_key(data.id) != True:
		rele1 = 0b11111 & data.id - 2
		GPIO.setup(rele1, GPIO.OUT)
		GPIO.output(rele1, OFF)
		map_lights[data.id] = [data.name, 0] #create the light

        
    else:
        if map_lights[data.id][1] != data.state:
            map_lights[data.id][1] = data.state
            releControl(data)
        if map_lights[data.id][0] != data.name:
            map_lights[data.id][0] = data.name
###########################################################

#broker_address="127.0.0.1"
#broker_address="192.168.1.6"
broker_address="10.42.0.1"
port = 1883
client = mqtt.Client("2")
client.on_message = on_message
client.connect(broker_address, port) #connect to broker
client.loop_start()


def mqtt_subscriber():

    rospy.init_node('mqtt_subscriber', anonymous=True)
    client.subscribe("json")
    rospy.spin()

if __name__ == '__main__':
    try:
        mqtt_subscriber()
    except rospy.ROSInterruptException:
		GPIO.cleanup()
		client.disconnect()
		client.loop_stop()
		pass
