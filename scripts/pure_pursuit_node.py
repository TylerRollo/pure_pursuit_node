#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import numpy as np
import csv
import os
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA

# TODO CHECK: include needed ROS msg type headers and libraries

class PurePursuit(Node):
    """ 
    Implement Pure Pursuit on the car
    This is just a template, you are free to implement your own node!
    """
    def __init__(self):
        super().__init__('pure_pursuit_node')
        # TODO: create ROS subscribers and publishers
        # Create a publisher for driving commands
        self.drive_publisher = self.create_publisher(
            AckermannDriveStamped,
            '/drive',
            10
        )

        # Create a subscriber to Pose data
        self.subscription_odom = self.create_subscription(
            Odometry, 
            '/ego_racecar/odom', 
            self.odom_callback, 
            10
        )
        
        # Create a publisher to Marker data
        self.marker_publisher = self.create_publisher(
            MarkerArray,
            '/visualization_marker_array',
            10
        )

        self.lookahead = 1
        
        self.markers = self.load_markers(csv_path=os.getcwd()+'/src/pure_pursuit_node/data.csv')
        self.publish_markers()        

    def load_markers(self, csv_path):
        markers = [] 
        with open(csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                markers.append([row[0], row[1], row[2]])

        return markers
    
    def publish_markers(self):
        marker_array = MarkerArray()
        for idx, (x, y, z) in enumerate(self.markers):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = 'markers'
            marker.id = idx
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = float(x)
            marker.pose.position.y = float(y)
            marker.pose.position.z = 0.0
            marker.scale.x = 0.1
            marker.scale.y = 0.1
            marker.scale.z = 0.1
            marker.color = ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0)
            marker_array.markers.append(marker)
            self.get_logger().info(f'{marker.pose.position.x, marker.pose.position.y} loaded.')
        self.marker_publisher.publish(marker_array)


    def odom_callback(self, odom_msg):
        current_position = np.array(odom_msg.pose.pose.position.x, odom_msg.pose.pose.position.y)
        self.get_logger().info(f'{current_position[0], current_position[1]} is the current x, y position.')
    
        # TODO: find the current waypoint to track using methods mentioned in lecture

        

        # TODO: transform goal point to vehicle frame of reference

        # TODO: calculate curvature/steering angle
        curvature = (2*abs(current_position[1]))/(self.lookahead^2)

        # TODO: publish drive message, don't forget to limit the steering angle
        drive_msg = AckermannDriveStamped()
        drive_msg.drive.steering_angle = np.clip(curvature, -.3, .3)
        drive_msg.drive.speed = drive_msg.drive.steering_angle
        self.drive_publisher.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    print("PurePursuit Initialized")
    pure_pursuit_node = PurePursuit()
    rclpy.spin(pure_pursuit_node)

    pure_pursuit_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
