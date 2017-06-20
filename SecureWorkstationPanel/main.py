import sys
import threading

from PyQt4.QtGui import *
import Xlib.display
import Xlib.X

from ui_secureworkstationpanel import *


class SecureWorkstationPanel(Ui_SecureWorkstationPanel, QWidget):
    def __init__(self):
        super(Ui_SecureWorkstationPanel, self).__init__()
        self.setupUi(self)

        self.resize(QtGui.QDesktopWidget().screenGeometry().width(), 100)
        self.move(0, 0)
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)

    def reserve_space(self):
        def _f():
            self._display = Xlib.display.Display()
            self._window = self._display.create_resource_object('window',
                                                                self.winId())
            self._window.change_property(
                self._display.intern_atom('_NET_WM_STRUT'),
                self._display.intern_atom('CARDINAL'),
                32, [0, 0, 100, 0], Xlib.X.PropModeReplace)
            self._window.change_property(
                self._display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                self._display.intern_atom('CARDINAL'),
                32, [0, 0, 100, 0], Xlib.X.PropModeReplace)
        thread = threading.Thread(target=_f)
        thread.start()


def main():
    global app
    app = QApplication(sys.argv)

    global panel
    panel = SecureWorkstationPanel()

    panel.show()
    panel.reserve_space()

    app.exec_()


if __name__ == "__main__":
    main()
