#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pure_pursuit_node',  
            executable='pure_pursuit_node.py',  
            name='pure_pursuit_node',  
            output='screen',
        )
    ])
