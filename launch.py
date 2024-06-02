# This script is responsible for running all the necessary components to operate the Drone.
# =------------------------------=
# Author: Broteen Das

# GLOBAL PARAMETERS:-

START_SIM = 1
START_SITL = 1


SIM_VEHICLE_PATH = "~/ardupilot/Tools/autotest/sim_vehicle.py" # !NOT USED below
MODEL_PATH = ""
WORLDS_PATH = ""

                                     # $simvehicle_path
LAUNCH_SITL_COMMAND = "python3 ~/gh_repos/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON"
# LAUNCH_SITL_COMMAND = "python3 ~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON"
LAUNCH_SIMULATION_COMMAND = "gz sim -r iris_runway_custom.sdf"
ROS_GZ_BRIDGE_COMMAND = "ros2 run ros_gz_bridge parameter_bridge /camera@sensor_msgs/msg/Image[gz.msgs.Image"


THREAD_SIM = None
THREAD_SITL = None
THREAD_BRIDGE = None

# 0. Imports
import os
import threading
import subprocess
from time import sleep

# 1. Arm the environment variables
print("Adding to ENV")
os.environ["GZ_SIM_RESOURCE_PATH"] = f"{os.environ['GZ_SIM_RESOURCE_PATH']}:{os.environ['PWD']}/models:{os.environ['PWD']}/worlds"



# 2. Startup the ROS_GZGARDEN bridge
# os.system("ros2 topic list")
THREAD_BRIDGE = threading.Thread(target = lambda: os.system(ROS_GZ_BRIDGE_COMMAND))
THREAD_BRIDGE.start()

# 3. Fire the SITL and SIM
# def fireSITL():
#     os.system(LAUNCH_SITL_COMMAND)
def fireSIM():
    os.system(LAUNCH_SIMULATION_COMMAND)

THREAD_SIM = threading.Thread(target=fireSIM)
THREAD_SITL = threading.Thread(target=lambda: subprocess.call(['gnome-terminal', '--', 'python3', '-c', f'import os; os.system("{LAUNCH_SITL_COMMAND}")']))

if START_SIM:
    THREAD_SIM.start()
if START_SITL:
    sleep(5)
    THREAD_SITL.start()