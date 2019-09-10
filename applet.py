#!/usr/bin/python2
import signal
import subprocess
import time
from threading import Thread
from collections import defaultdict

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject as gobject


APPINDICATOR_ID = 'wpm-x11'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_label("text", "widest text")
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(_):
    notify.uninit()
    gtk.main_quit()

count = defaultdict(lambda : 0)

def get_bucket(t):
    return int(round(t))

def update_code():
    global count
    start_time = get_bucket(time.time())
    UPDATE_INTERVAL = 2
    TIME_HORIZON = [60*60, 15*60, 5*60, 60, 10]
    HORIZON_NAME = ["1h", "15m", "5m", "1m", "10s"]
    max_10s = 0
    while True:
        time.sleep(UPDATE_INTERVAL)
        now = get_bucket(time.time())
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
            c = count[now - t]
            total += c
            t += 1
        print ""
        for tt in range(1, UPDATE_INTERVAL + 10):
            count.pop(now - t - tt, 0)  # erase element if it exists

def update_thread():
    thread = Thread(target = update_code)
    thread.setDaemon(True)
    thread.start()

def listen_code():
    global count
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
            count[get_bucket(t)] += 1
    print("xinput pipe closed")

def listen_thread():
    thread = Thread(target = listen_code)
    thread.setDaemon(True)
    thread.start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gobject.threads_init()
    listen_thread()
    update_thread()
    main()
