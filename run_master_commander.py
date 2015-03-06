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


FILE_TO_READ = "/dev/shm/master_and_commander/curr_command.p"

def cb(data):
    print "Received: " + str(data)
    pickle.dump( data, open( FILE_TO_READ, "wb" ) )


if __name__ == '__main__':
    rospy.init_node('master_writer')
    rospy.Subscriber(PUB_TOPIC, Twist, cb)
    rospy.spin()

