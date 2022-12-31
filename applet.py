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
        self.indicator.set_tooltip_text("collecting data...")
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

    def set_text(self, text):
        self.indicator.set_tooltip_text(text)

    def quit(self, _):
        notify.uninit()
        gtk.main_quit()


def main():
    keyRecorder = KeyRecorder()
    appletIcon = AppletIcon()
    keyRecorder.connect("statistics", lambda obj, text: appletIcon.set_text(text))
    keyRecorder.start()
    gtk.main()

class DaemonThread:
    def __init__(self, code, threadName = None):
        self.thread = Thread(target = code, name = threadName)
        self.thread.setDaemon(True)
    def start(self):
        self.thread.start()

class KeyRecorder(gobject.GObject):
    __gsignals__ = {
        'statistics': (gobject.SIGNAL_RUN_FIRST, None, (str,))
    }

    count = defaultdict(lambda : 0)

    def __init__(self):
        gobject.GObject.__init__(self)
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
        TIME_HORIZON = [18*60*60,12*60*60, 6*60*60, 60*60, 15*60, 5*60, 60, 10]
        HORIZON_NAME = ["18h", "12h", "6h", "1h", "15m", "5m", "1m", "10s"]
        max_10s = 0
        while True:
            time.sleep(UPDATE_INTERVAL)
            now = self.get_bucket(time.time())
            total = 0
            horizon = len(TIME_HORIZON) - 1
            t = 0
            output = ''
            while horizon >= 0:
                if(t == TIME_HORIZON[horizon]):
                    #window = (now - start_time + 1) if (now - t) < start_time else t
                    window = t
                    rate = total * 1.0 / window * 60
                    max_10s = max(max_10s, rate)
                    if(horizon + 1 == len(TIME_HORIZON)):
                        print("MAX %5.1f/min," % (max_10s), end='')
                        output += "%5.1f/min MAX\n" % (max_10s)
                    print("%5.1f/min @%s (%4d), " % (rate, HORIZON_NAME[horizon], total), end='')
                    output += "%5.1f/min @%-3s (%4d)\n" % (rate, HORIZON_NAME[horizon], total)
                    horizon -= 1
                    continue
                c = self.count[now - t]
                total += c
                t += 1
            print("")
            output = output.rstrip()
            self.emit("statistics", output)
            for tt in range(1, UPDATE_INTERVAL + 10):
                self.count.pop(now - t - tt, 0)  # erase element if it exists

    def listen_code(self):
        while True:
            #KEYBOARD_NAME = 'Lite-On Goldtouch USB Keyboard'  # run xinput to determine this
            #KEYBOARD_NAME = 'Lite-On Technology Corp. Goldtouch USB Keyboard'  # run xinput to determine this
            KEYBOARD_NAME = "11"
            #KEYBOARD_NAME = 'Topre REALFORCE 87 US'  # run xinput to determine this
            KEYBOARD_NAME = subprocess.check_output(["/bin/bash", "-c", "/usr/bin/xinput | perl -ne 'if(/Lite-On Technology Corp. Goldtouch USB Keyboard\s+id=(\d+)/) { print \"$1\"; exit }'"]).decode("utf-8")

            xinput = subprocess.Popen(["/usr/bin/xinput", "test", KEYBOARD_NAME],
                stdout=subprocess.PIPE)
            print("xinput pipe open, listening for keys from '" + KEYBOARD_NAME + "'")
            while True:
                line = xinput.stdout.readline()
                if not line: break

                col = line.split()
                if(len(col) == 3 and col[1] == b'press'):
                    t = time.time()
                    #print(t, col[2])
                    self.count[self.get_bucket(t)] += 1
            time.sleep(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gobject.threads_init()
    main()
