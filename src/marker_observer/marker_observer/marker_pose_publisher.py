import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose

import cv2
from cv2 import aruco

import numpy as np

import tf_transformations

class MarkerObserver(Node):
    def __init__(self):
        super().__init__('marker_pose_publisher_node')
        self.publisher_ = self.create_publisher(Pose,'marker_pose',10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cap = cv2.VideoCapture(0)

        self.marker_length = 0.071
        self.dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        self.cameraMatrix = np.array(
            [[664.93960093,0.0,301.55176042],
 [0.0, 670.76186604,224.96345292],
 [0.0, 0.0         ,1.0]])
        self.distCoeffs = np.array([3.53489812e-01,-2.81250343e+00,-2.64818258e-03,-6.65322506e-03,7.75799051e+00])
        
    def timer_callback(self):
        ret, frame = self.cap.read()

        if ret == True:
            cv2.imshow('img',frame)
            cv2.waitKey(1)
            corners, ids, _ = aruco.detectMarkers(frame, self.dict_aruco, parameters=self.aruco_parameters)
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.marker_length, self.cameraMatrix, self.distCoeffs)

            if ids is not None and ids[0][0] == 0:
                pose = Pose()
                pose.position.x = tvecs[0][0][0]
                pose.position.y = tvecs[0][0][1]
                pose.position.z = tvecs[0][0][2]

                rot_matrix = np.eye(4)
                rot_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvecs[0][0]))[0]
                quat = tf_transformations.quaternion_from_matrix(rot_matrix)

                pose.orientation.x = quat[0]
                pose.orientation.y = quat[1]
                pose.orientation.z = quat[2]
                pose.orientation.w = quat[3]

                self.publisher_.publish(pose)

def main():
    rclpy.init()
    node = MarkerObserver()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



def main(args=None):
    rclpy.init(args=args)

    publisher = MarkerObserver()

    rclpy.spin(publisher)
    
    publisher.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()