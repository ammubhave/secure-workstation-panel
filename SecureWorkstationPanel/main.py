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
        self.urlbar.returnPressed.connect(self.urlbar_navigate)

        def change_button_clicked():
            self.activateWindow()
            self.urlbar.setFocus(True)
        self.change_button.clicked.connect(change_button_clicked)

        self._display = Xlib.display.Display()
        self._root = self._display.screen().root

        self.set_prompt_q = Queue.Queue()
        self.set_prompt_thread = SetPromptWorker(self.set_prompt_q)
        self.connect(self.set_prompt_thread,
                     SIGNAL('setPrompt(QString, PyQt_PyObject)'),
                     self.set_prompt)
        self.set_prompt_thread.start()

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

    def urlbar_navigate(self):
        names = ewmh.get_desktop_names().reply()[:-1]
        n = ewmh.get_number_of_desktops().reply() + 1
        ewmh.request_number_of_desktops_checked(n).check()
        url = str(self.urlbar.text())
        with open('/var/run/qubes/dispid') as f:
            names.append("disp" + f.read() + "|" + url)
        ewmh.set_desktop_names_checked(map(lambda x: x.encode('utf-8'),
                                           names + [""])).check()
        ewmh.request_current_desktop_checked(n - 1).check()

        def _navigate(url):
            subprocess.call("echo 'firefox %s' | "
                            "/usr/lib/qubes/qfile-daemon-dvm "
                            "qubes.VMShell dom0 DEFAULT "
                            "red" % (urllib.quote(url.encode('utf8'))),
                            shell=True)
        thread = threading.Thread(target=_navigate,
                                  args=[str(self.urlbar.text())])
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
    panel.active_workspace_change_listen()
    panel.secure_workstation_netfilter_daemon_listen()

    app.exec_()


if __name__ == "__main__":
    main()
