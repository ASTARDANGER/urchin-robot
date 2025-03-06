import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    # Define the path to the URDF and the Gazebo world
    urdf_file = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'robot.urdf'
    )

    world_file = os.path.join(
        get_package_share_directory('my_robot_description'),
        'world',
        'world.world'
    )

    # Define the path to the controller configuration (controller.yaml)
    controller_yaml = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'controller.yaml'
    )

    # Declare the launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Read the URDF file for the robot description
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()


    joint_state_publisher = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        parameters=[{'robot_description': robot_desc}, controller_yaml],
        remappings=[('/controller_manager', '/controller_manager')],
        output='screen'
    )

    # Define the robot_state_publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Spawn the robot in Gazebo (this is handled by ros_gz_sim package)
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-string', robot_desc,
            '-x', '0.0', '-y', '0.0', '-z', '0.1',  # Positioning the robot
            '-R', '0.0', '-P', '0.0', '-Y', '0.0',
            '-name', 'robot'
        ]
    )

    # Return the launch description with the necessary nodes
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation time'),
        # Lancer Gazebo avec le monde
        ExecuteProcess(
            cmd=['gz', 'sim', world_file],
            output='screen'
        ),
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
    ])
