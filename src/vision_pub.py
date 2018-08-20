import rospy
import cv2
import sys
import numpy as np
import roslib
from sensor_msg.msg import String
from cv_bridge import CvBridge, CvBridgeError


class camStream():
    def __init__(self):
        self.node_name = "camStream"
        # rospy.init_node(self.node_name)
        self.image_pub = rospy.Publisher("ImageTopic",GreyImg)
        self.bridge = CvBridge()
        rospy.on_shutdown(self.cleanup)
        rospy.loginfo("Connecting to Camera Stream")

    def cameraStream(self):
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            rosimg = self.bridge.cv2_to_image(gray , "bgr8")
            try:
                self.image_pub.publish(rosimg)
            except CvBridgeError as e:
                print(e)
            cv2.imshow(self.node_name, gray)
            cv2.waitKey()
            break
        cap.release()
        cv2.destroyAllWindows()

    def cleanup(self):
        print("Shutting down vision node.")
        cv2.destroyAllWindows()




def main(args):
    rospy.init_node('camStream', anonymous = True)
    try:
        camStream().cameraStream()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down vision node.")
        cv2.DestroyAllWindows()

if __name__ == '__main__':
main(sys.argv)
