#!/usr/bin/python2
import signal
import json
import subprocess
from threading import Thread
import time


from urllib2 import Request, urlopen, URLError

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
    item_joke = gtk.MenuItem('Joke')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def fetch_joke():
    request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
    response = urlopen(request)
    joke = json.loads(response.read())['value']['joke']
    return joke

def joke(_):
    notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

def listen_code():
    print("xinput pipe opening")
    xinput = subprocess.Popen(["/usr/bin/xinput", "test", 'Lite-On Goldtouch USB Keyboard'],
        stdout=subprocess.PIPE)
    while True:
        line = xinput.stdout.readline()
        if not line: break
        
        col = line.split()
        if(len(col) == 3 and col[1] == 'press'):
            t = time.time()
            print t, col[2]
    print("xinput pipe closed")

def listen_thread():
    thread = Thread(target = listen_code)
    thread.setDaemon(True)
    thread.start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gobject.threads_init()
    listen_thread()
    main()
