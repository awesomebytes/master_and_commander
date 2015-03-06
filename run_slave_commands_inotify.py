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
import pyinotify
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

    wm = pyinotify.WatchManager()  # Watch Manager
    #   mask = pyinotify.ALL_EVENTS #pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
    mask = pyinotify.IN_CLOSE_WRITE # We care of every time something in the folder (so just curr_command.p) is closed writting

    WATCH_DIR = '/dev/shm/master_and_commander'

    class EventHandler(pyinotify.ProcessEvent):
        def my_init(self, publisher):
            #print "publisher is: " + str(publisher)
            self.pub = publisher

        def process_IN_CLOSE_WRITE(self, event):
            #print "IN_CLOSE_WRITE happened! Loading file..."
            msg_sent = False
            while not msg_sent:
                try:
                    msg = pickle.load( open( FILE_TO_READ, "rb" ))
                    msg_sent = True
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    #print "Error pickle load, try again"
                    pass
            #print "Publishing message!"
            self.pub.publish(msg)

    event_handler = EventHandler(publisher=pub)

    notifier = pyinotify.Notifier(wm, event_handler)
    wdd = wm.add_watch(WATCH_DIR, mask, rec=True)

    notifier.loop() # This keeps looping waiting for events :D



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


    