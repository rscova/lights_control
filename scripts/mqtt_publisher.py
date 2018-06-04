#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json
import requests
import time

from std_msgs.msg import String
from lights_control.msg import LightingControl

time_last1 = 0
time_last2 = 0

map_lights = {};
map_lights[0000] = {" ", 0}

#broker_address="127.0.0.1"
broker_address="192.168.1.7"
port = 1883
keepalive = 45
topic_publish = "control_lights"

ubidots_broker = "things.ubidots.com"
token = "A1E-bA1OGoaWvlXyVINAAOk9xNWrf5sbAS"  # Put your TOKEN here
device_label = "monitoring-lights"  # Put your device label here

# Payload to send to Ubidots
def build_payload(light):
    payload = {light.name: {"value": light.state,"context":{"id":light.id}}}
    return payload

# Send request to Ubidots
def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, device_label)
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")

    print("[INFO] request made properly, your device is updated")

# Define on_connect event Handler
def on_connect(self, mosq, obj, rc):
	print "Connected to MQTT Broker"

# Define on_connect UBIDOTS event Handler
def on_connect_ubidots(self, mosq, obj, rc):
	print "Connected to MQTT Ubidots Broker"

# Define on_publish event Handler
def on_publish(client, userdata, mid):
    print "Message Published..."

# Initiate MQTT Client
mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.connect(broker_address, port, keepalive)
mqttc.loop_start()

# Initiate MQTT Ubidots Client
mqttu = mqtt.Client()
mqttu.on_publish = on_publish
mqttu.on_connect = on_connect_ubidots
mqttu.username_pw_set(token, token)
mqttu.connect(ubidots_broker, port, keepalive)
mqttu.loop_start()


def callback(light):
    #rospy.loginfo("I heard %s %s %s", light.id, light.name, light.state)
    global time_last1
    global time_last2
    global map_lights

    if map_lights.has_key(light.id) != True:
        map_lights[light.id] = [light.name, light.state] #create the light
        sent_mqtt_message(light)

    elif map_lights[light.id][1] != light.state:
        map_lights[light.id][1] = light.state
        sent_mqtt_message(light)

    else:
        if (time.time() - time_last1) > 10:
            l1 = LightingControl(1101,map_lights[1101][0],map_lights[1101][1])
            sent_mqtt_message(l1)

        if (time.time() - time_last2) > 10:
            l2 = LightingControl(1102,map_lights[1102][0],map_lights[1102][1])
            sent_mqtt_message(l2)


def sent_mqtt_message(light):
    payload = build_payload(light)
    payload2 = json.dumps({"id":light.id, "name":light.name, "state":light.state})
    mqttc.publish("control_lights", payload2);
    post_request(payload)
    global time_last1
    global time_last2

    if light.id == 1101:
        time_last1 = time.time()
    elif light.id == 1102:
        time_last2 = time.time()




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
