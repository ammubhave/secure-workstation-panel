import os.path
import Queue
import signal
import subprocess
import sys
import threading
import urllib

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Xlib.display
import Xlib.X
import xpybutil.ewmh as ewmh

from ui_secureworkstationpanel import *

import evdev
from evdev import InputDevice, categorize, ecodes

class SetPromptWorker(QThread):
    def __init__(self, q):
        QThread.__init__(self)
        self.q = q

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            message, clientsocket = self.q.get(True)
            print(message, clientsocket)
            self.emit(SIGNAL('setPrompt(QString, PyQt_PyObject)'),
                      message, clientsocket)
        self.terminate()

class SetUrlWorker(QThread):
    def __init__(self, q):
        QThread.__init__(self)
        self.q = q

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            url = self.q.get(True)
            self.emit(SIGNAL('setUrl(QString)'), url)
        self.terminate()

class SecureWorkstationPanel(Ui_SecureWorkstationPanel, QWidget):
    def __init__(self):
        super(Ui_SecureWorkstationPanel, self).__init__()
        self.setupUi(self)

        self.resize(QtGui.QDesktopWidget().screenGeometry().width(), 150)
        self.move(0, 0)
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.prompt.hide()

        def change_button_clicked():
            def _f():
                dev = InputDevice('/dev/input/by-id/usb-Logitech_USB_Receiver-event-kbd')
                scancodes = {
                    0: None, 1: None, 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
                    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: None, 15: None, 16: u'q', 17: u'w', 18: u'e', 19: u'r',
                    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: None, 29: None,
                    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
                    40: u'"', 41: u'`', 42: None, 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
                    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: None, 56: None, 57: u' ', 100: None
                }
                dev.grab()
                s = ''
                for event in dev.read_loop():
                    if event.type == ecodes.EV_KEY:
                        data = categorize(event)
                        if data.keystate == 1:
                            key_lookup = scancodes.get(data.scancode, None)
                            if key_lookup != None:
                                s += key_lookup
                            if data.scancode == 14 and len(s) > 0:
                                s = s[:-1]
                            self.set_url_q.put(s)
                            if(data.scancode == 28):
                                print(s)
                                self.urlbar_navigate(s)
                                break
                dev.ungrab()
                dev.close()
            thread = threading.Thread(target=_f)
            thread.start()
        self.change_button.clicked.connect(change_button_clicked)

        self._display = Xlib.display.Display()
        self._root = self._display.screen().root

        self.set_prompt_q = Queue.Queue()
        self.set_prompt_thread = SetPromptWorker(self.set_prompt_q)
        self.connect(self.set_prompt_thread,
                     SIGNAL('setPrompt(QString, PyQt_PyObject)'),
                     self.set_prompt)
        self.set_prompt_thread.start()

        self.set_url_q = Queue.Queue()
        self.set_url_thread = SetUrlWorker(self.set_url_q)
        self.connect(self.set_url_thread,
                     SIGNAL('setUrl(QString)'),
                     self.set_url)
        self.set_url_thread.start()

    def set_url(self, url):
        self.urlbar.setText(url)

    def set_prompt(self, message, clientsocket):
        print(message)
        self.message.setText(message)

        def allow_clicked():
            clientsocket.send('\x01')
            clientsocket.close()
            self.prompt.hide()

        def deny_clicked():
            clientsocket.send('\x00')
            clientsocket.close()
            self.prompt.hide()
        self.allow_button.clicked.connect(allow_clicked)
        self.deny_button.clicked.connect(deny_clicked)
        self.urlbar.setFocusPolicy(Qt.StrongFocus)
        self.prompt.show()

    def active_workspace_change_listen(self):
        self._root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

        def _f():
            NET_CURRENT_DESKTOP = self._display.intern_atom(
                '_NET_CURRENT_DESKTOP')
            while True:
                event = self._display.next_event()
                if (event.type == Xlib.X.PropertyNotify and
                        event.atom == NET_CURRENT_DESKTOP):
                    workspace_id = \
                        self._root.get_full_property(
                            NET_CURRENT_DESKTOP,
                            Xlib.X.AnyPropertyType).value[0]
                    if workspace_id == 0:
                        self.urlbar.setText('')
                    else:
                        names = ewmh.get_desktop_names().reply()[:-1]
                        url = names[workspace_id].split('|', 1)[-1]
                        self.urlbar.setText(url)
                        print(names[workspace_id])
        thread = threading.Thread(target=_f)
        thread.start()

    def urlbar_navigate(self, url):
        names = ewmh.get_desktop_names().reply()[:-1]
        n = ewmh.get_number_of_desktops().reply() + 1
        ewmh.request_number_of_desktops_checked(n).check()

        next_dispid = '1'
        if os.path.exists('/var/run/qubes/dispid'):
            with open('/var/run/qubes/dispid') as f:
                next_dispid = f.read()
        names.append("disp" + next_dispid + "|" + url)
        ewmh.set_desktop_names_checked(map(lambda x: x.encode('utf-8'),
                                           names + [""])).check()
        ewmh.request_current_desktop_checked(n - 1).check()

        def _navigate(url):
            subprocess.call("echo 'firefox %s' | "
                            "/usr/lib/qubes/qfile-daemon-dvm "
                            "qubes.VMShell dom0 DEFAULT "
                            "red" % (urllib.quote(url.encode('utf8'))),
                            shell=True)
        thread = threading.Thread(target=_navigate, args=[url])
        thread.start()


    def reserve_space(self):
        def _f():
            self._window = self._display.create_resource_object('window',
                                                                self.winId())
            self._window.change_property(
                self._display.intern_atom('_NET_WM_STRUT'),
                self._display.intern_atom('CARDINAL'),
                32, [0, 0, 150, 0], Xlib.X.PropModeReplace)
            self._window.change_property(
                self._display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                self._display.intern_atom('CARDINAL'),
                32, [0, 0, 150, 0], Xlib.X.PropModeReplace)
            subprocess.call(["/usr/bin/xprop",
                             "-f", "_NET_WM_WINDOW_TYPE", "32a",
                             "-id", str(self.winId()),
                             "-set", "_NET_WM_WINDOW_TYPE",
                             "_NET_WM_WINDOW_TYPE_DOCK"])
        thread = threading.Thread(target=_f)
        thread.start()

    def secure_workstation_netfilter_daemon_listen(self):
        def _f():
            import socket
            HOST = 'localhost'
            PORT = 10293
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(1)
            while 1:
                (clientsocket, address) = s.accept()
                r = ''
                while True:
                    b = clientsocket.recv(1)
                    if b == '\x00':
                        break
                    r += b

                src_vm, dst = r.strip().split()

                self.set_prompt_q.put(('Connection attempt to ' + dst +
                                       ' from ' + src_vm,
                                       clientsocket))

                print(src_vm, r)
                # clientsocket.send('\x01')
                # clientsocket.close()
        thread = threading.Thread(target=_f)
        thread.start()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    global app
    app = QApplication(sys.argv)

    global panel
    panel = SecureWorkstationPanel()

    ewmh.request_number_of_desktops_checked(1).check()

    panel.show()
    panel.reserve_space()
    #panel.active_workspace_change_listen()
    #panel.secure_workstation_netfilter_daemon_listen()

    #window = QX11EmbedWidget()
    #window.resize(QtGui.QDesktopWidget().screenGeometry().width(), 200)
    #panel.setParent(window)
    #window.embedInto(18874413)
    #window.show()

    app.exec_()


if __name__ == "__main__":
    main()
