#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json

from std_msgs.msg import String
from lights_control.msg import LightingControl

data = LightingControl(1111,'light',0)
data_string =  str(data.id) + " " + data.name + " "+str(data.state)

broker_address="localhost"
client = mqtt.Client("1")
client.connect(broker_address) #connect to broker
client.loop_start()

def callback(dato):
    data = dato
    rospy.loginfo("I heard %s %s %s", data.id, data.name, data.state)

    data_string =  str(data.id) + " " + data.name + " "+str(data.state)
    client.publish("msgs",data_string)#publish
    payload = json.dumps({"id":data.id, "name":data.name, "state":data.state})
    client.publish("json", payload);

def mqtt_publisher():

    rospy.init_node('mqtt_publisher', anonymous=True)
    rospy.Subscriber("lights_status", LightingControl, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        mqtt_publisher()
    except rospy.ROSInterruptException:
        client.disconnect()
        client.loop_stop()
        pass
