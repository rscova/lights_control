################################################################################
# CMake
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(lights_control)

################################################################################
# Packages
################################################################################
find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
  roscpp
  rospy
)

################################################################################
# Declare ROS messages, services and actions
################################################################################
add_message_files(
  FILES
  LightingControl.msg
  LightingControlStamped.msg
)

add_service_files(
  FILES
  ChangeLightStatus.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

################################################################################
# Catkin specific configuration
################################################################################
catkin_package(
  CATKIN_DEPENDS std_msgs message_runtime
)

################################################################################
# Build
################################################################################
include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(controller src/controller.cpp)
target_link_libraries(controller ${catkin_LIBRARIES})
