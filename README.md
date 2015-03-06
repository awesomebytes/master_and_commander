master_and_commander
===

"Simple" scripts making possible passing one topic (currently just `Twist`) from one roscore to 
other roscores.

For example... you have your local roscore `http://localhost:11311`

And you want to send the same message at the same time (kinda) to another robot `http://lolcathost:11311` (lolcathost could be myrobot) and also maybe
to another simulation in your computer `http://localhost:113399`.

So you run:

	run_master_commander.py

Which subscribes to a topic, in my case `/key_vel` and it writes on a file at `/dev/shm/master_and_commander/curr_command.p` (it's shared memory, not disk, so it's way faster). The .p extension is because I'm pickling the message. If you try to pickle a message with a timestamp it doesn't work, I need to look into it.

Then run:

	run_slave_commands_inotify.py lolcathost http://localhost:113399

You'll see that if you are using the standard ROS port (11311) you can just put the robot name, if you are doing something different,
just write the full URL.

This will set a inotify watcher on the folder `/dev/shm/master_and_commander/` and for every closing of file (hopefully only our file) it
will load it and publish that message. This happens for every host given in the command.

For a publication rate of:

	average rate: 10.005
	min: 0.063s max: 0.114s std dev: 0.02245s window: 620

The slaves publish at:

	average rate: 9.996
	min: 0.015s max: 0.114s std dev: 0.02265s window: 400


In my tests.


# Why did I do this?
Because if I try to communicate with a socket after doing `rospy.init_node()` it doesn't work. It never connects. Seems like rospy takes over all the socketing stuff. (Which reminds me I should copy here the scripts with my trials on making it work).


TODO: Make sure the folder exists in /dev/shm, if not, create it.

TODO: Unify everything into a single node (so they can both know what folder to watch, probably a random name)

TODO: Generalize for any topic

TODO: Generalize for any topic type (must fight with timestamp problem)
