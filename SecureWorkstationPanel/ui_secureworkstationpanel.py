# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'secureworkstationpanel.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SecureWorkstationPanel(object):
    def setupUi(self, SecureWorkstationPanel):
        SecureWorkstationPanel.setObjectName(_fromUtf8("SecureWorkstationPanel"))
        SecureWorkstationPanel.resize(708, 158)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SecureWorkstationPanel.sizePolicy().hasHeightForWidth())
        SecureWorkstationPanel.setSizePolicy(sizePolicy)
        SecureWorkstationPanel.setAutoFillBackground(True)
        self.gridLayout = QtGui.QGridLayout(SecureWorkstationPanel)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.change_button = QtGui.QPushButton(SecureWorkstationPanel)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_button.sizePolicy().hasHeightForWidth())
        self.change_button.setSizePolicy(sizePolicy)
        self.change_button.setObjectName(_fromUtf8("change_button"))
        self.verticalLayout.addWidget(self.change_button)
        self.urlbar = QtGui.QLineEdit(SecureWorkstationPanel)
        self.urlbar.setMinimumSize(QtCore.QSize(0, 32))
        self.urlbar.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.urlbar.setFont(font)
        self.urlbar.setObjectName(_fromUtf8("urlbar"))
        self.verticalLayout.addWidget(self.urlbar, QtCore.Qt.AlignTop)
        self.prompt = QtGui.QFrame(SecureWorkstationPanel)
        self.prompt.setFrameShape(QtGui.QFrame.StyledPanel)
        self.prompt.setFrameShadow(QtGui.QFrame.Raised)
        self.prompt.setObjectName(_fromUtf8("prompt"))
        self.gridLayout_2 = QtGui.QGridLayout(self.prompt)
        self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.message = QtGui.QLabel(self.prompt)
        self.message.setWordWrap(True)
        self.message.setObjectName(_fromUtf8("message"))
        self.horizontalLayout_2.addWidget(self.message)
        self.allow_button = QtGui.QPushButton(self.prompt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allow_button.sizePolicy().hasHeightForWidth())
        self.allow_button.setSizePolicy(sizePolicy)
        self.allow_button.setObjectName(_fromUtf8("allow_button"))
        self.horizontalLayout_2.addWidget(self.allow_button)
        self.deny_button = QtGui.QPushButton(self.prompt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deny_button.sizePolicy().hasHeightForWidth())
        self.deny_button.setSizePolicy(sizePolicy)
        self.deny_button.setObjectName(_fromUtf8("deny_button"))
        self.horizontalLayout_2.addWidget(self.deny_button)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.prompt)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(SecureWorkstationPanel)
        QtCore.QMetaObject.connectSlotsByName(SecureWorkstationPanel)

    def retranslateUi(self, SecureWorkstationPanel):
        SecureWorkstationPanel.setWindowTitle(_translate("SecureWorkstationPanel", "SecureWorkstationPanel", None))
        self.change_button.setText(_translate("SecureWorkstationPanel", "Change URL", None))
        self.message.setText(_translate("SecureWorkstationPanel", "Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? Do you want to allow www.google.com? ", None))
        self.allow_button.setText(_translate("SecureWorkstationPanel", "Allow", None))
        self.deny_button.setText(_translate("SecureWorkstationPanel", "Deny", None))

