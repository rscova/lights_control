#include <iostream>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include "lights_control/LightingControl.h"
#include "lights_control/ChangeLightStatus.h"


bool toogleLight(lights_control::ChangeLightStatus::Request &req,
								 lights_control::ChangeLightStatus::Response &res)
{
	return true;
}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "controller");
	ros::Rate loop_rate(0.5);

	ros::NodeHandle n;

	ros::Publisher lights_status_pub = n.advertise<lights_control::LightingControl>("lights_status", 1000);
	ROS_INFO("Ready /lights_status Topic");

	ros::ServiceServer service = n.advertiseService("change_light_status", toogleLight);
  ROS_INFO("Ready /change_light_status Service");


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
