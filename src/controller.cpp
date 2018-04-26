#include <iostream>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include "lights_control/LightingControl.h"
#include "lights_control/ChangeLightStatus.h"


lights_control::LightingControl msg;

bool toogleLight(lights_control::ChangeLightStatus::Request &req,
								 lights_control::ChangeLightStatus::Response &res
							   )
{
	if(msg.id == req.id)
	{
		msg.state = req.state;
		if(msg.state == req.state)
			res.result = res.OK;
	}

	else
		res.result = res.ERROR;

	return true;
}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "controller");
	ros::NodeHandle n;

	ros::Publisher lights_status_pub = n.advertise<lights_control::LightingControl>("lights_status", 1000);
	ROS_INFO("Ready /lights_status Topic");

	ros::ServiceServer service = n.advertiseService("change_light_status",toogleLight);
  ROS_INFO("Ready /change_light_status Service");

	ros::Rate loop_rate(0.5);

	msg.id = 10;
	msg.name = "luces_habitacion";
	msg.state = msg.ON;

	while (ros::ok())
	{
		lights_status_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}

	return 0;
}
