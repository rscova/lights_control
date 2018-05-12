#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
import json
import time
import ssl

from std_msgs.msg import String
from lights_control.msg import LightingControl


# MQTT Variables
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC_PUBLISH = "monitoring"
MQTT_TOPIC_SUBSCRIBE = "control"

# Ubidots Variables
TOKEN = "A1E-JIhfhKtgOzHiPD6qXpkQpRONljvyFM"  # Put your TOKEN here
DEVICE_LABEL = "raspberry-pi"  # Put your device label here
VARIABLE_LABEL_1 = "temperature"  # Humidity variable
VARIABLE_LABEL_2 = "humidity"  # Temperature variable
VARIABLE_LABEL_3 = "light" # Light variable

# MQTT Ubidots
MQTT_UBIDOTS_BROKER = "things.ubidots.com"
MQTT_UBIDOTS_PORT = 1883
MQTT_UBIDOTS_SUBSCRIBE = "/v1.6/devices/"+DEVICE_LABEL+"/"+VARIABLE_LABEL_3+"/lv"

# Initialize DHT22 Adafruit sensor
#sensor = Adafruit_DHT.DHT22
# GPIO for DHT22
#pin = 4

# Payload to send to Ubidots
def build_payload(value_1, value_2):
    payload = {VARIABLE_LABEL_1: value_1,
               VARIABLE_LABEL_2: value_2}
    return payload

# Send request to Ubidots
def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")

    print("[INFO] request made properly, your device is updated")

# Define on_connect event Handler
def on_connect(self, mosq, obj, rc):
	print "Connected to MQTT Broker"
	mqttc.subscribe(MQTT_TOPIC_SUBSCRIBE, 0)

# Define on_connect UBIDOTS event Handler
def on_connect_ubidots(self, mosq, obj, rc):
	print "Connected to MQTT Ubidots Broker"
	mqttu.subscribe(MQTT_UBIDOTS_SUBSCRIBE, 0)

# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
    print "Subscribed to topic: %s" % (MQTT_TOPIC_SUBSCRIBE)

# Define on_publish event Handler
def on_publish(client, userdata, mid):
    print "Message Published..."

# Define on_message event Handler
def on_message(mosq, obj, msg):
    print msg.payload
    data = json.loads(msg.payload)
    if "type" in data:
        if data["type"] == "light":
            if "data" in data:
                # GPIO.setup(11, GPIO.IN)
                # status = GPIO.input(11)
                # GPIO.setup(11, GPIO.OUT)
                # GPIO.output(11, data["data"])
                data=True
                if data["data"] is True:
                    jsonObject = {
                        "type": "light",
                        "data": "true"
                        }
                    payload = {VARIABLE_LABEL_3: "1.0"}
                else:
                    jsonObject = {
                        "type": "light",
                        "data": "false"
                        }
                    payload = {VARIABLE_LABEL_3: "0.0"}
                post_request(payload)
                data_string = json.dumps(jsonObject)
                # Publish message to MQTT Topic
                print data_string
                mqttc.publish(MQTT_TOPIC_PUBLISH, data_string)
    else:
        print msg.payload

# Define on_message event Handler
def on_message_ubidots(mosq, obj, msg):
    print msg.payload
    # GPIO.setup(11, GPIO.OUT)
    if msg.payload == "1":
        print "entro al if de 1"
        jsonObject = {
            "type": "light",
            "data": "true"
            }
        # GPIO.output(11, True)
          print("envio True")
    else:
        jsonObject = {
            "type": "light",
            "data": "false"
            }
       # GPIO.output(11, False)
         print("envio False")
    data_string = json.dumps(jsonObject)
    # Publish message to MQTT Topic
    print data_string
    mqttc.publish(MQTT_TOPIC_PUBLISH, data_string)


# Initiate MQTT Client
mqttc = mqtt.Client()

# Register Event Handlers
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()

# Initiate MQTT Ubidots Client
mqttu = mqtt.Client()

# Register Event Handlers
mqttu.on_publish = on_publish
mqttu.on_connect = on_connect_ubidots
mqttu.on_subscribe = on_subscribe
mqttu.on_message = on_message_ubidots

# Connect with MQTT Broker
mqttu.username_pw_set(TOKEN, TOKEN)
mqttu.connect(MQTT_UBIDOTS_BROKER, MQTT_UBIDOTS_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttu.loop_start()



def callback(dato):
    data = dato
    rospy.loginfo("I heard %s %s %s", data.id, data.name, data.state)
    payload = json.dumps({"id":data.id, "name":data.name, "state":data.state})
    client.publish(topic, payload)


def listener():
    rospy.init_node('mqtt_publisher', anonymous=True)
    rospy.Subscriber("lights_status", LightingControl, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        client.disconnect()
        client.loop_stop()
        pass
