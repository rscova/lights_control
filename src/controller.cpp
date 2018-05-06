#include <iostream>
#include <string>
#include <vector>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include "lights_control/LightingControl.h"
#include "lights_control/LightingControl.h"
#include "lights_control/ChangeLightStatus.h"
#include "lights_control/ChangeLightName.h"


using namespace std;

vector<lights_control::LightingControl> v_lights;
lights_control::LightingControl light;

bool toogleLight(lights_control::ChangeLightStatus::Request &req,
								 lights_control::ChangeLightStatus::Response &res)
{
	bool error = true;
	for(int i = v_lights.size()-1; i >= 0; i--)
	{
		if(v_lights[i].id == req.id)
		{
			v_lights[i].state = req.state;
			error = false;
		}
	}

	if(error)
		res.result = res.ERROR;
	else
		res.result = res.OK;

	return true;
}

bool changeLightName(lights_control::ChangeLightName::Request &req,
								 		 lights_control::ChangeLightName::Response &res)
{
	bool error = true;
	for(int i = v_lights.size()-1; i >= 0; i--)
	{
		if(v_lights[i].id == req.id)
		{
			v_lights[i].name = req.name;
			error = false;
		}
	}

	if(error)
		res.result = res.ERROR;
	else
		res.result = res.OK;

	return true;
}

bool createNewLight(lights_control::ChangeLightName::Request &req,
								 		 lights_control::ChangeLightName::Response &res)
{
	bool error = false;
	for(int i = v_lights.size()-1; i >= 0; i--)
		if(v_lights[i].id == req.id or v_lights[i].name == req.name)
			error = true;

	if(error)
		res.result = res.ERROR;
	else
	{
		light.id = req.id;
		light.name = req.name;
		light.state = light.OFF;
		v_lights.push_back(light);

		res.result = res.OK;
	}

 return true;
}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "controller");
	ros::NodeHandle n;
	ros::Rate loop_rate(1);

	ros::Publisher lights_status_pub = n.advertise<lights_control::LightingControl>("lights_status", 1000);
	ROS_INFO("Ready /lights_status Topic");

	ros::ServiceServer service1 = n.advertiseService("change_light_status",toogleLight);
  ROS_INFO("Ready /change_light_status Service");
	ros::ServiceServer service2 = n.advertiseService("change_light_name",changeLightName);
	ROS_INFO("Ready /change_light_name Service");
	ros::ServiceServer service3 = n.advertiseService("create_new_light",createNewLight);
	ROS_INFO("Ready /create_new_light Service");


	int id = 0;
	string name = "";
	int state = 0;
	n.param("id",    id, 1101);

	n.param("name",  name, std::string("first_light"));
	n.param("state",  state, 0);

	light.id = id;
	light.name = name;
	light.state = state;

	v_lights.push_back(light);

	light.id = 1102;
	light.name = "cocina";
	light.state = 0;

	v_lights.push_back(light);

	while (ros::ok())
	{
		loop_rate = ros::Rate(v_lights.size());
		for(int i = v_lights.size()-1; i >= 0; i--)
		{
			lights_status_pub.publish(v_lights[i]);
			ros::spinOnce();
			loop_rate.sleep();
		}
	}

	return 0;
}
