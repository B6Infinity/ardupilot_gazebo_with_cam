# This script is responsible for running all the necessary components to operate the Drone.
# =------------------------------=
# Author: Broteen Das

import sys

# GLOBAL PARAMETERS:-

START_SITL = None
START_SIM = None
gaz_verbose = ''

if '-sim' in sys.argv:
    START_SIM = 1
    START_SITL = 0
elif '-sitl' in sys.argv:
    START_SIM = 0
    START_SITL = 1
else:
    START_SIM = 1
    START_SITL = 1

if '-v' in sys.argv:
    gaz_verbose = '-v 4'




WORLD = "aerothon_ground2.sdf" # or you can switch to 'iris_runway_custom.sdf'
SIM_VEHICLE_PATH = "~/ardupilot/Tools/autotest/sim_vehicle.py" # !NOT USED below
MODEL_PATH = ""
WORLDS_PATH = ""

                                     # $simvehicle_path
LAUNCH_SITL_COMMAND = "python3 ~/gh_repos/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON"
# LAUNCH_SITL_COMMAND = "python3 ~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON"
LAUNCH_SIMULATION_COMMAND = f"gz sim -r {WORLD} {gaz_verbose}"
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
    print("Starting SIM...")
    THREAD_SIM.start()
if START_SITL:
    sleep(5)
    print("Starting SITL...")
    THREAD_SITL.start()

print("All threads started successfully! You should see 3 terminals in total including this one (3rd terminal takes a bit of time to load)...")