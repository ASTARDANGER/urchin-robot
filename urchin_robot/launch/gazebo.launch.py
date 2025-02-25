import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    pkg_my_robot = get_package_share_directory('urchin_robot')

    # Convert package:// to an absolute path
    urdf_file = os.path.join(pkg_my_robot, 'urdf', 'robot.urdf')

    # Ensure Gazebo gets an absolute path for STL files
    with open(urdf_file, 'r') as file:
        urdf_content = file.read()

    # Save the modified URDF to a temporary file
    tmp_urdf_path = os.path.join(pkg_my_robot, 'urdf', 'robot.urdf')
    with open(tmp_urdf_path, 'w') as file:
        file.write(urdf_content)

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', urdf_file],
            output='screen'
        ),
    ])
