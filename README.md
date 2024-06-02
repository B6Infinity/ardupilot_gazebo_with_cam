# Make sure to have the following installed:

- Gazebo Sim 7 (Garden)
    - https://gazebosim.org/docs/garden/install
- ROS 2 Humble
    - https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
- ROS Humble - Gazebo Garden Bridge
    - `sudo apt install ros-humble-ros-gzgarden-bridge`

# Understanding the Workflow

There are 2 main files:
- `launch.py`
    - Launches all the processes required for the development (the *SITL, simulation* and the *ros_gzgarden_bridge* to get the **/camera** topic from gz sim)
- `dev.py`
    - This is the file where you do your image processing. This file is the boiler plate where you get the `frame` variable as an `np.ndarray` and you do the conventional image processing that you would generally do.

The drone is stationary upon launch and can be controlled from a seperate terminal via Dronekit.