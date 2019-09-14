#!/usr/bin/python2
import signal
import subprocess
import time
from threading import Thread
from collections import defaultdict

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify
from gi.repository import GObject as gobject

class AppletIcon:
    APPINDICATOR_ID = 'wpm-x11'
    menu = None

    def __init__(self):
        self.indicator = gtk.StatusIcon()
        self.indicator.set_from_stock(gtk.STOCK_INFO)
        self.indicator.set_has_tooltip(True)
        self.indicator.set_tooltip_text("testing")
        self.indicator.connect('popup-menu', self.on_popup)
        self.menu = self.build_menu()

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def on_popup(self, icon, button, time):
        self.menu.popup(None, None, gtk.StatusIcon.position_menu, icon, button, time)

    def quit(self, _):
        notify.uninit()
        gtk.main_quit()


def main():
    appletIcon = AppletIcon()
    gtk.main()

class DaemonThread:
    def __init__(self, code, threadName = None):
        self.thread = Thread(target = code, name = threadName)
        self.thread.setDaemon(True)
    def start(self):
        self.thread.start()

class KeyRecorder:
    count = defaultdict(lambda : 0)

    def __init__(self):
        self.listen_thread = DaemonThread(self.listen_code, "listen-thread")
        self.update_thread = DaemonThread(self.update_code, "update-thread")

    def start(self):
        self.listen_thread.start()
        self.update_thread.start()

    def get_bucket(self, t):
        return int(round(t))

    def update_code(self):
        start_time = self.get_bucket(time.time())
        UPDATE_INTERVAL = 2
        TIME_HORIZON = [60*60, 15*60, 5*60, 60, 10]
        HORIZON_NAME = ["1h", "15m", "5m", "1m", "10s"]
        max_10s = 0
        while True:
            time.sleep(UPDATE_INTERVAL)
            now = self.get_bucket(time.time())
            total = 0
            horizon = len(TIME_HORIZON) - 1
            t = 0
            while horizon >= 0:
                if(t == TIME_HORIZON[horizon]):
                    #window = (now - start_time + 1) if (now - t) < start_time else t
                    window = t
                    rate = total * 1.0 / window * 60
                    max_10s = max(max_10s, rate)
                    if(horizon + 1 == len(TIME_HORIZON)):
                        print "MAX %5.1f/min," % (max_10s),
                    print "%5.1f/min @%s (%4d), " % (rate, HORIZON_NAME[horizon], total),
                    horizon -= 1
                    continue
                c = self.count[now - t]
                total += c
                t += 1
            print ""
            for tt in range(1, UPDATE_INTERVAL + 10):
                self.count.pop(now - t - tt, 0)  # erase element if it exists

    def listen_code(self):
        print("xinput pipe opening")
        xinput = subprocess.Popen(["/usr/bin/xinput", "test", 'Lite-On Goldtouch USB Keyboard'],
            stdout=subprocess.PIPE)
        while True:
            line = xinput.stdout.readline()
            if not line: break

            col = line.split()
            if(len(col) == 3 and col[1] == 'press'):
                t = time.time()
                #print t, col[2]
                self.count[self.get_bucket(t)] += 1
        print("xinput pipe closed")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gobject.threads_init()
    KeyRecorder().start()
    main()
