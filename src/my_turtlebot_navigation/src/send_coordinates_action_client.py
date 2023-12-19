#!/usr/bin/env python 

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseActionGoal , MoveBaseAction , MoveBaseActionFeedback , MoveBaseGoal
import get_coordinates_service_server



class send_coordinates(object):
    def __init__(self,x):
        self.client = actionlib.SimpleActionClient('/move_base',MoveBaseAction)
        self.client.wait_for_server()
        self.data_to_be_sent = MoveBaseGoal()
        self.data_to_be_sent.target_pose.header.frame_id = 'map'
        self.data_to_be_sent.target_pose.pose = x

    def action_goal(self):
        rospy.loginfo('sending the goal now')
        self.client.send_goal(self.data_to_be_sent)



if __name__ == "__main__":
    rospy.init_node('SendCoordinates')
    rospy.spin()