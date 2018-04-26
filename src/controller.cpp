#include <iostream>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include "lights_control/LightingControl.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "controller");
	ros::NodeHandle n;
	ros::Publisher lights_status_pub = n.advertise<lights_control::LightingControl>("lights_status", 1000);
	ros::Rate loop_rate(0.5);

	lights_control::LightingControl msg;

	msg.id_number = 10;
	msg.id_name = "luces_habitacion";
	msg.state = msg.ON;

	while (ros::ok())
	{
		lights_status_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}

	return 0;
}
