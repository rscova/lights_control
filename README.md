# LIGHTS CONTROLLER

This repository contains a ROS node for a House lighting control. The aim of this proyect
is connect two machines running a roscore each one.


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

Compile the package: $cd ~/catkin_ws && catkin_make --only-pkg-with-deps lights_control

In machine one (M1) run roscore and launch the light control node:
 $ roslaunch ligths_control lights_control.launch node_name:=light_controller

You can see the topic /ligth_status

In other terminal of M1 run: $ rosrun lights_control mqtt_publisher.py

In M2 run roscore: $ roscore

Still in M2 run in other terminal: raspy_controller.py

**Useful information:**
 


