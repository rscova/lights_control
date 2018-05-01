#include <iostream>
#include <string>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include "lights_control/LightingControl.h"
#include "lights_control/LightingControlStamped.h"
#include "lights_control/ChangeLightStatus.h"
#include "lights_control/ChangeLightName.h"



lights_control::LightingControlStamped msg;

bool toogleLight(lights_control::ChangeLightStatus::Request &req,
								 lights_control::ChangeLightStatus::Response &res)
{
	if(msg.data.id == req.id)
	{
		msg.data.state = req.state;

		if(msg.data.state == req.state)
			res.result = res.OK;
	}

	else
		res.result = res.ERROR;

	return true;
}

bool changeLightName(lights_control::ChangeLightName::Request &req,
								 		 lights_control::ChangeLightName::Response &res)
{
	if(msg.data.id == req.id)
	{
		msg.data.name = req.name;

		if(msg.data.name == req.name)
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

	ros::Publisher lights_status_pub = n.advertise<lights_control::LightingControlStamped>("lights_status", 1000);
	ROS_INFO("Ready /lights_status Topic");

	ros::ServiceServer service1 = n.advertiseService("change_light_status",toogleLight);
  ROS_INFO("Ready /change_light_status Service");
	ros::ServiceServer service2 = n.advertiseService("change_light_name",changeLightName);
	ROS_INFO("Ready /change_light_name Service");

	ros::Rate loop_rate(10);

	int id = 0;
	std::string name = "";
	int state = 0;
	n.param("id",    id, 1);

	n.param("name",  name, std::string("first_light"));
	n.param("state",  state, 0);

	msg.data.id = id;
	msg.data.name = name;
	msg.data.state = state;

	while (ros::ok())
	{
		lights_status_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}

	return 0;
}
