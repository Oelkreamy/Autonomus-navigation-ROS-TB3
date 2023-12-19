# #!/usr/bin/env python 

# import rospy
# from my_turtlebot_navigation.srv import MyServiceMessage , MyServiceMessageResponse
# import os 
# import yaml 
# from geometry_msgs.msg import Pose
# import send_coordinates_action_client

# class get_coordinates(object):

#     def __init__(self):
#         self.server = rospy.Service("/get_coordinates" , MyServiceMessage , self.callback)
#         self.response = MyServiceMessageResponse()
#         self.coordinates = Pose()
#         self.data = {}
#     def callback(self,request):

#         self.label = request.label
#         os.chdir("/home/user/catkin_ws/src/my_turtlebot_localization/config")
#         with open('spots.txt', 'r') as file:
#             self.data.update(yaml.safe_load(file))

#         for item in self.data:
#             if item == self.label:
#                 self.coordinates.position.x = self.data[item]['position']['x']
#                 self.coordinates.position.y = self.data[item]['position']['y']
#                 self.coordinates.position.z = self.data[item]['position']['z']
#                 self.coordinates.orientation.z = self.data[item]['orientation']['z']
#                 self.coordinates.orientation.w = self.data[item]['orientation']['w']
#                 print(self.coordinates)
             
#             x = send_coordinates_action_client.send_coordinates(self.coordinates)
#             x.action_goal()
#             self.response.navigation_successfull = True
#             self.response.message = 'ok'
           
#         return self.response 

        

# if __name__ == "__main__":
#     rospy.init_node("service_node")
#     get_coordinates()
#     rospy.spin()


#!/usr/bin/env python3 

import rospy
from my_turtlebot_navigation.srv import MyServiceMessage , MyServiceMessageResponse
from std_msgs.msg import String
import os 
import yaml 
from geometry_msgs.msg import Pose
import send_coordinates_action_client

class get_coordinates(object):

    def __init__(self):
        self.server = rospy.Service("/get_coordinates" , MyServiceMessage , self.callback)
        self.listener = rospy.Subscriber("/chatter", String, self.listener_callback)
        self.talker = rospy.Publisher("/operation", String, queue_size=10)
        self.operation = String()
        self.op_result = String()
        self.done = "Done"
        self.rate=rospy.Rate(30)
        self.response = MyServiceMessageResponse()
        self.coordinates = Pose()
        self.data = {}

    def listener_callback(self, msg):
        self.op_result = msg
    def callback(self,request):

        self.label = request.label
        os.chdir("/home/user/catkin_ws/src/my_turtlebot_localization/config")
        with open('spots.txt', 'r') as file:
            self.data.update(yaml.safe_load(file))
        
         
        if self.label == "seeds":
            
            for item in self.data:
                self.coordinates.position.x = self.data[item]['position']['x']
                self.coordinates.position.y = self.data[item]['position']['y']
                self.coordinates.position.z = self.data[item]['position']['z']
                self.coordinates.orientation.z = self.data[item]['orientation']['z']
                self.coordinates.orientation.w = self.data[item]['orientation']['w']
                print(self.coordinates)
             
                x = send_coordinates_action_client.send_coordinates(self.coordinates)
                x.action_goal()
                x.client.wait_for_result()
                self.operation.data = "drill_drop"
                self.talker.publish(self.operation)
                
                while self.op_result.data != self.done:
                    self.rate.sleep()

                self.response.navigation_successfull = True
                self.response.message = 'ok'

        else:   

            for item in self.data:
                if item == self.label:
                    self.coordinates.position.x = self.data[item]['position']['x']
                    self.coordinates.position.y = self.data[item]['position']['y']
                    self.coordinates.position.z = self.data[item]['position']['z']
                    self.coordinates.orientation.z = self.data[item]['orientation']['z']
                    self.coordinates.orientation.w = self.data[item]['orientation']['w']
                    print(self.coordinates)
                 
                x = send_coordinates_action_client.send_coordinates(self.coordinates)
                x.action_goal()
                x.client.wait_for_result()
                self.response.navigation_successfull = True
                self.response.message = 'ok'
               
            
        return self.response 

        

if __name__ == "__main__":
    rospy.init_node("service_node")
    get_coordinates()
    rospy.spin()