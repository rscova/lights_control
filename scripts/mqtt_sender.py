#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json
import time
import ssl

from std_msgs.msg import String
from lights_control.msg import LightingControl


def on_connect(client, userdata, flags, rc):

    if rc == 0:
        rospy.loginfo("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection

    else:
        rospy.loginfo("Connection failed")

def on_publish(client, userdata, result):
	rospy.loginfo("Published!")



data = LightingControl(1111,'light',0)
Connected = False
broker_address= "things.ubidots.com"
port = 8883
user = "A1E-bA1OGoaWvlXyVINAAOk9xNWrf5sbAS"
password = ""
topic = "/v1.6/devices/mqtt"
client = mqtt.Client()
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, port=port)
client.loop_start()


def callback(dato):
    data = dato
    rospy.loginfo("I heard %s %s %s", data.id, data.name, data.state)
    payload = json.dumps({"id":data.id, "name":data.name, "state":data.state})
    client.publish(topic, payload)


def listener():

    rospy.init_node('mqtt_publisher', anonymous=True)

    rospy.Subscriber("lights_status", LightingControl, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        client.disconnect()
        client.loop_stop()
        pass
