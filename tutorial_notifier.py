# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.ALL_EVENTS #pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

WATCH_DIR = '/dev/shm/master_and_commander'
# class EventHandler(pyinotify.ProcessEvent):
#     def process_IN_CREATE(self, event):
#         print "Creating:", event.pathname
#
#     def process_IN_DELETE(self, event):
#         print "Removing:", event.pathname

p = pyinotify.PrintAllEvents()

# handler = EventHandler()
notifier = pyinotify.Notifier(wm, p)# handler)
wdd = wm.add_watch(WATCH_DIR, mask, rec=True)

notifier.loop()
