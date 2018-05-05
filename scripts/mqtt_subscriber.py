#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json

from std_msgs.msg import String
from lights_control.msg import LightingControl

data = LightingControl(1111,'light',0)
data_string =  str(data.id) + " " + data.name + " "+str(data.state)


def on_message(client, userdata, message):
    rospy.loginfo("message received: %s" ,str(message.payload.decode("utf-8")))
    rospy.loginfo("message topic: %s",message.topic)
    rospy.loginfo("message qos: %s",message.qos)
    rospy.loginfo("message retain flag: %s",message.retain)


broker_address="192.168.1.4"
port = 1883
client = mqtt.Client("2")
client.on_message = on_message
client.connect(broker_address, port) #connect to broker
client.loop_start()


def mqtt_subscriber():

    rospy.init_node('mqtt_subscriber', anonymous=True)
    client.subscribe("json")
    rospy.loginfo("Subscribed")
    rospy.spin()

if __name__ == '__main__':
    try:
        mqtt_subscriber()
    except rospy.ROSInterruptException:
        client.disconnect()
        client.loop_stop()
        pass
