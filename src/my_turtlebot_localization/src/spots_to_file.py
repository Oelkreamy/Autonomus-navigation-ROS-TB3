#! /usr/bin/env python 

import rospy 
from my_turtlebot_localization.srv import  MyServiceMessage , MyServiceMessageResponse 
from geometry_msgs.msg import PoseWithCovarianceStamped
import os 

class spot_recording(object):

    def __init__(self):

        self.spots = PoseWithCovarianceStamped()
        self.recording = False
        self.file_name = 'spots.txt'
        self.spot_recorded = False
        self.result = MyServiceMessageResponse()
        self.i = 0
        self.poses_dict = {}
        self.pose_name_list = []
        self.server = rospy.Service('/save_spot',MyServiceMessage, self.callback)
        self.sub = rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.msg_callback)
        x = self.sub.get_num_connections()
        while self.sub.get_num_connections() < 1:
            rospy.logwarn(self.sub.get_num_connections())
            rospy.loginfo("Waiting for subscriber to connect...")
            rospy.sleep(1)


    def msg_callback(self, msg):
        self.spots = msg.pose.pose


    def callback(self, request):
        
        if not self.recording:

            self.recording = True
            self.pose_name = request.label
            

            if self.pose_name != 'end':
                rospy.loginfo("Started recording the spot")

                if self.i < 3:
                    
                    self.pose_name_list.append(self.pose_name)
                    self.pose_dict = {self.pose_name:{'position':{'x':self.spots.position.x,'y':self.spots.position.y,'z':self.spots.position.z},'orientation':{'x':self.spots.orientation.x,'y':self.spots.orientation.y,'z':self.spots.orientation.z,'w':self.spots.orientation.w}}}
                    self.i+=1
                    rospy.logwarn(self.pose_dict)
                    self.recording = False
                    self.poses_dict.update(self.pose_dict)
                    self.result.navigation_successfull = True
                    self.result.message = 'pose saved succesfully'
                    return self.result
                   
                else:
                    rospy.logwarn("you reached the limit of poses that can be saved")
      
            elif self.pose_name == 'end':

                os.chdir("/home/user/catkin_ws/src/my_turtlebot_localization/config")
                with open(self.file_name, 'w') as file:
                    for item in self.pose_name_list:
                        file.write("{}: \n position:\n  x: {}\n  y: {}\n  z: {} \n orientation:\n  z: {}\n  w: {} \n".format(item,str(self.poses_dict[item]['position']['x']),str(self.poses_dict[item]['position']['y']),str(self.poses_dict[item]['position']['z']),str(self.poses_dict[item]['orientation']['z']),str(self.poses_dict[item]['orientation']['w'])))
                
                print("File saved successfully")
                self.i=0
                self.recording = False
                self.result.navigation_successfull = True 
                self.result.message = 'The operation has been done succesfully'    

                return self.result
                    
                
  

if __name__ == "__main__":

    rospy.init_node('spot_recorder')
    spot_recording()
    rospy.spin()
    




