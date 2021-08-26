#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from itertools import chain
# from kobuki msgs.msg import BumperEvent

pub = None
laser_range = 3.5
threshold = 1.0
threshold_s = 1.8
min_window_length = 5

linear_speed = 0.35
angular_speed = 0.2


# def clbk_bumper(msg):
#    if msg.state == BumperEvent.PRESSED:
#        print("bumper pressed")

def clbk_laser(msg):
    laser_list = []
    windows_list = []

    avg_left = min(msg.ranges[87], msg.ranges[88], msg.ranges[89], msg.ranges[90], msg.ranges[91], msg.ranges[92])
    avg_right = min(msg.ranges[267], msg.ranges[268], msg.ranges[269], msg.ranges[270], msg.ranges[271],
                    msg.ranges[272])
    avg_front = min(msg.ranges[0], msg.ranges[4], msg.ranges[9], msg.ranges[350], msg.ranges[355], msg.ranges[359])

    if avg_front < 0.5:
        if avg_left < avg_right:
            print("f imp turn to right")
            vel = Twist()
            vel.linear.x = 0
            vel.angular.z = -angular_speed
            pub.publish(vel)
            return
        else:
            print("f imp turn to left")
            vel = Twist()
            vel.linear.x = 0
            vel.angular.z = angular_speed
            pub.publish(vel)
            return

    if avg_left < 0.5 and avg_front < 1.5:
        print("imp turn to right")
        vel = Twist()
        vel.linear.x = 0
        vel.angular.z = -angular_speed
        pub.publish(vel)
        return

    if avg_right < 0.5 and avg_front < 1.5:
        print("imp turn to left")
        vel = Twist()
        vel.linear.x = 0
        vel.angular.z = angular_speed
        pub.publish(vel)
        return

    for i in range(len(msg.ranges)):
        laser_list.append(laser_range - min(msg.ranges[i], laser_range))

    special_window = []
    special_window_found = False
    # special case
    for_range = chain(range(331, 359), range(0, 29))
    for i in for_range:
        if laser_list[i] <= threshold_s:
            special_window.append(i)
        else:
            if len(special_window) != 0:
                if len(special_window) > min_window_length:
                    special_window_found = True
                special_window = []
        

    if special_window_found or len(special_window) > 50:
        print("special window found")
        vel = Twist()
        vel.linear.x = linear_speed
        vel.angular.z = 0
        pub.publish(vel)
        return

    current_window = []
    for i in range(len(laser_list)):
        if laser_list[i] <= threshold:
            current_window.append(i)
        else:
            if len(current_window) != 0:
                if len(current_window) > min_window_length:
                    windows_list.append(current_window)
                current_window = []

    if len(windows_list) == 0:
        print("no window found")
        return

    means = []
    for window in windows_list:
        start = window[0]
        end = window[len(window) - 1]
        mean = (start + end) // 2
        means.append(mean)

    rem = []
    for mean in means:
        if 0 <= mean < 180:
            rem.append(mean)
        else:
            rem.append(360 - mean)

    min_rem = 1000
    min_rem_index = -1
    for i in range(len(rem)):
        if rem[i] < min_rem:
            min_rem = rem[i]
            min_rem_index = i

    if means[min_rem_index] < 180:
        print("turn to left")
        vel = Twist()
        vel.linear.x = 0
        vel.angular.z = angular_speed
        pub.publish(vel)
    else:
        print("turn to right")
        vel = Twist()
        vel.linear.x = 0
        vel.angular.z = -angular_speed
        pub.publish(vel)


def main():
    global pub

    print("hi")
    rospy.init_node('velocity_controller')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    # bump_sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, clbk_bumper)
    
    rospy.spin()


if __name__ == '__main__':
    main()

