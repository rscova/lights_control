# LIGHTS CONTROLLER

This repository contains a ROS node for a House lighting control.


### Setup instructions

Install mosquitto (MQTT): $ sudo apt-get install mosquitto mosquitto-clients

Install the paho library for Python: $ sudo pip install paho-mqtt

Download this repo in your catkin workspace


**Check your MQTT instalation:**

Create a local broker: $ sudo service mosquitto start

Publish in a topic: $ mosquitto_pub -h [broker's IP] -t [your topic] -m "Hello MQTT!"
Example: $ mosquitto_pub -h 127.0.0.1 -t msgs -m "Hello MQTT!"

Subscribe to a topic: $ mosquitto_sub -h [broker's IP] -t [your topic]

For subscribe to all topics: $ mosquitto_sub -t '#'


**How to use this Package:**
