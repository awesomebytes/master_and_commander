#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 3/5/15

@author: sampfeiffer

run_slave_commands.py contains...
"""
__author__ = 'sampfeiffer'

# System imports
import os
import sys
import math
import numpy as np
from copy import deepcopy
#import threading
from multiprocessing import Process
import cPickle as pickle
#import pyinotify
from cStringIO import StringIO

# Local imports

# ROS imports
import rospy
from actionlib import SimpleActionClient
from actionlib import SimpleActionServer
import tf.transformations

# ROS messages imports
from std_msgs.msg import Header
from actionlib_tutorials.msg import FibonacciAction, FibonacciGoal, FibonacciResult, FibonacciFeedback
from std_srvs.srv import Empty, EmptyRequest, EmptyResponse
from geometry_msgs.msg import Twist


PUB_TOPIC = '/key_vel'


# class SlaveReaderAndPublisher():
#     """This class does stuff"""
#
#     def __init__(self):
#         # Topics
#         rospy.loginfo("Setting publisher to " + PUB_TOPIC)
#         self.pub_topic = rospy.Publisher(PUB_TOPIC, Header, queue_size=1)

FILE_TO_READ = "/dev/shm/master_and_commander/curr_command.p"

def read_and_publish(uri):
    print "arg received: " + uri
    os.environ['ROS_MASTER_URI'] = uri
    rospy.init_node('node', anonymous=True)
    pub = rospy.Publisher(PUB_TOPIC, Twist, queue_size=1)

    # last_msg = None
    while not rospy.is_shutdown():
        try:
            # f = open( FILE_TO_READ, "rb" )
            # n_bytesread = len(f.read(1))
            # f.close()
            # if n_bytesread > 0:
            #     print "More than 0bytes!: " + str(n_bytesread)
            f = open( FILE_TO_READ, "rb" )
            msg_read = StringIO(f.read())
            print len(msg_read.getvalue())
            if len(msg_read.getvalue()) > 0:
                print "We load because there is something to load"
                msg = pickle.load( msg_read )
            else:
                print "ERRORRRRRRRRRR NOTHING TO LOAD"
        except IOError:
            rospy.logwarn("Error (no " + FILE_TO_READ + " yet)")
            rospy.sleep(0.2)
            continue
        # if last_msg == msg: # maybe we need a better comparison
        #     # Same message, we do nothing
        #     print "Same message, doing nothing"
        #     continue # we could subscribe to file changes to get a callback
        # else:

        pub.publish(msg)
        # last_msg = msg


def usage():
    print "Usage:"
    print sys.argv[0] + " URI1 URI2 URI3"
    print "\n Example:"
    print sys.argv[0] + " http://localhost:11311 http://localhost:11322"
    print "\n Or put the robot name if it's the same port"
    print sys.argv[0] + " reemh3-2c ant-4c"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit(0)
    robot_uris = []
    for idx, uri in enumerate(sys.argv):
        if idx > 0:
            if "http://" in uri:
                robot_uris.append(uri)
            else:
                robot_uris.append("http://" + uri + ":11311")

    print "Robot uris to re-send stuff:"
    print robot_uris

    for uri in robot_uris:
        print "Current uri is: " + uri
        print "Launching process"
        p = Process(target=read_and_publish, args = (uri,))
        p.start()

    print "Done launching processes"


    