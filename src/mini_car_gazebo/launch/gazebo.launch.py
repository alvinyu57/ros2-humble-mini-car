import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node


def generate_launch_description():
    mini_car_description_dir = get_package_share_directory('mini_car_description')
    mini_car_gazebo_dir = get_package_share_directory('mini_car_gazebo')
    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')

    xacro_file = os.path.join(
        mini_car_description_dir,
        'urdf',
        'mini_car.urdf.xacro'
    )

    world_file = os.path.join(
        mini_car_gazebo_dir,
        'worlds',
        'empty.world'
    )

    robot_description_content = Command([
        'xacro ',
        xacro_file
    ])

    robot_description = {
        'robot_description': robot_description_content
    }

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            robot_description,
            {'use_sim_time': True}
        ]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -v 4 {world_file}'
        }.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        parameters=[{
            'world': 'empty_world',
            'string': robot_description_content,
            'name': 'mini_car',
            'x': 0.0,
            'y': 0.0,
            'z': 0.075
        }],
        output='screen'
    )

    delayed_spawn = TimerAction(
        period=3.0,
        actions=[spawn_entity]
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        delayed_spawn
    ])
