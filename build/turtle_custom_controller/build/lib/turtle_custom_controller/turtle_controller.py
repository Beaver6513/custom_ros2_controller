#!/usr/bin/env python3

import rclpy
from pynput.keyboard import Listener
from rclpy.node import Node
from geometry_msgs.msg import Twist

# classe publisher
class custom_controller(Node):
    def __init__(self):
        super().__init__("customController")
        self.test_pub_ = self.create_publisher(Twist,"/turtle1/cmd_vel", 10)
        #self.timer_ = self.create_timer(1.0/60.0, self.send_transform)
        self.get_logger().info("Custom Controller started")
        self.msg = Twist()
    
    # durante on_press (pynput event) modifica msg e lo pubblica
    # permette di gestire più key contemporaneamente
    def on_press(self, key):
        if key.char == 'w':
            self.msg.linear.x = float(1)
        elif key.char == 's':
            self.msg.linear.x = float(-1)
        elif key.char == 'a':
            self.msg.angular.z = float(1)
        elif key.char == 'd':
            self.msg.angular.z = float(-1)
        #self.get_logger().info("OnPress triggered")
        self.test_pub_.publish(self.msg)
    
    # resetta msg quando la key viene rilasciata
    def on_release(self, key):
        #self.get_logger().info("OnRelease triggered")
        if key.char == 'w':
            self.msg.linear.x = float(0)
        elif key.char == 's':
            self.msg.linear.x = float(0)
        elif key.char == 'a':
            self.msg.angular.z = float(0)
        elif key.char == 'd':
            self.msg.angular.z = float(0)
        self.test_pub_.publish(self.msg)

    #def send_transform(self):
    #    self.test_pub_.publish(self.msg)


def main(args=None):
    # inizializza rclpy e crea l'object del nodo
    rclpy.init(args=args)

    controller = custom_controller()
    
    # crea il Listener per fare handling della tastiera
    with Listener(
        on_press=controller.on_press, 
        on_release=controller.on_release
    ) as listener:
        listener.join()
    
    # node loop
    rclpy.spin(controller)

    rclpy.shutdown()

if __name__ == "__main__":
    main()

