#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json

from std_msgs.msg import String
from lights_control.msg import LightingControl
from lights_control.srv import *

data = LightingControl(1111,'light',0)
data_string =  str(data.id) + " " + data.name + " "+str(data.state)

map_lights = {};
map_lights[0000] = {" ", 0}

def create_new_light_client(light):
    rospy.wait_for_service('create_new_light')
    try:
        create_new_light = rospy.ServiceProxy('create_new_light', CreateNewLight)
        resp1 = create_new_light(light.id,light.name)
        return resp1.result
    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s"%e)

def change_light_status_client(light):
    rospy.wait_for_service('change_light_status')
    try:
        change_light_status = rospy.ServiceProxy('change_light_status', ChangeLightStatus)
        resp1 = change_light_status(light.id,light.state)
        return resp1.result
    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s"%e)

def change_light_name_client(light):
    rospy.wait_for_service('change_light_name')
    try:
        change_light_name = rospy.ServiceProxy('change_light_name', ChangeLightName)
        resp1 = change_light_name(light.id,light.name)
        return resp1.result
    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s"%e)

def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8"))
    m_in = json.loads(m_decode)

    data.id = m_in["id"]
    data.name = str(m_in["name"])
    data.state = m_in["state"]

    #rospy.loginfo("message received: %s" ,m_in)
    #rospy.loginfo("message received: %s" ,str(message.payload.decode("utf-8")))
    #rospy.loginfo("message received: %s %s %s", m_in["id"], m_in["name"], m_in["state"])
    #rospy.loginfo("message topic: %s \n",message.topic)
    rospy.loginfo("message received: %s", data)

    if map_lights.has_key(data.id) != True:
        map_lights[data.id] = [data.name, data.state] #create the light
        create_new_light_client(data)
    else:
        if map_lights[data.id][1] != data.state:
            map_lights[data.id][1] = data.state
            change_light_status_client(data)
        if map_lights[data.id][0] != data.name:
            map_lights[data.id][0] = data.name
            change_light_name_client(data)
###########################################################

broker_address="192.168.1.4"
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
        client.disconnect()
        client.loop_stop()
        pass
