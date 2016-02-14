#!/usr/bin/env python

import os, time
import rospy
import google.protobuf.text_format

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectory
#from ros_pb2 import *
import ros_pb2
from machinekit import hal

# print ring properties
def print_ring(r):
    print 'information on the ring:'
    print ' - name=%s \n\
 - size=%d \n\
 - reader=%d \n\
 - writer=%d \n\
 - scratchpad=%d\n' % (r.name,r.size,r.reader,r.writer,r.scratchpad_size),
    print ' - use_rmutex=%d\n\
 - use_wmutex=%d \n\
 - type=%d \n\
 - in_halmem=%d' % (r.rmutex_mode, r.wmutex_mode,r.type,r.in_halmem)

# retrieve list of ring names
rings = hal.rings()
print '\navailable rings in HAL: \n   ', rings, '\n'

# Global variable for ring handle
r = 0
n = 0
#p = 0
#tp = None

def callback(data):

    print 'In callback'
    global n
    global r
    prev_point_time = 0.0
    tmp = 0
    for pose in data.points:
        tp = ros_pb2.JointTrajectoryPoint()
#        print pose.time_from_start
#        print ["P: {0:0.2e}".format(i) for i in pose.positions]
#        print ["V: {0:0.2e}".format(i) for i in pose.velocities]
#        print ["A: {0:0.2e}".format(i) for i in pose.accelerations]
#        print ["E: {0:0.2e}".format(i) for i in pose.effort]
        print ('tmp = %d' % tmp)
        point_time = float(pose.time_from_start.secs) \
                     + (float(pose.time_from_start.nsecs) / 1000000000 )

        tp.time_from_start = point_time
        tp.duration = point_time - prev_point_time
        tp.serial = int(n)
        print ('point time : %f' % tp.time_from_start)
        print ('duration   : %f' % tp.duration)
        print ('serial     : %i' % tp.serial)
        prev_point_time = point_time

        for j in range(len(pose.positions)):
            tp.positions.append(pose.positions[j])
            tp.velocities.append(pose.velocities[j])
            tp.accelerations.append(pose.accelerations[j])
            print pose.effort
            if not pose.effort:
                effort = 0.0
            else:
                effort = pose.effort[j]
            tp.effort.append(effort)
        print tp

        buffer = tp.SerializeToString()
        # put the point in the ring
        r.write(buffer)
        n += 1 #increase serial
        tmp += 1


def listener2():

    rospy.init_node('listener2', anonymous=True)
    if "joint_interpolator.traj" in rings:
        # attach to existing ring
        global r
        r = hal.Ring("joint_interpolator.traj")
        # see what we have
        print_ring(r)

    rospy.Subscriber("/joint_path_command", JointTrajectory, callback)
    rospy.spin()

if __name__ == '__main__':
    print 'Start of listener2, \n \
- subscribing to /joint_path_command \n'
    listener2()
