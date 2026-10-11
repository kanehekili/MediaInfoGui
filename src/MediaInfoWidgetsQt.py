# -*- coding: utf-8 -*-
'''
Created on May 01 2020

@author: kanehekili
'''
import sys
import os
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt6.QtGui import QFont
from MediaInfoGui import isHeader, formatForClipboard

class MediaInfoView(QMainWindow):

    def __init__(self,fileName):
        super(MediaInfoView,self).__init__()
        self.initUI(fileName)

    def initUI(self,fileName):
        self.setWindowTitle(fileName)
        palette = QApplication.palette()
        self.hdr_bg = palette.color(QtGui.QPalette.ColorRole.Highlight)
        self.hdr_fg = palette.color(QtGui.QPalette.ColorRole.HighlightedText)

        #the icon
        self.setWindowIcon(self.getAppIcon())

        self.table = self.createListWidget()
        clipBtn = QtWidgets.QPushButton("Clip")
        clipBtn.clicked.connect(self.callback_copy)
        okBtn = QtWidgets.QPushButton("OK")
        okBtn.clicked.connect(self.callback_btn_ok)

        buttonHBox = QtWidgets.QHBoxLayout()
        buttonHBox.setContentsMargins(0, 0, 0, 0)
        mainVBox = QtWidgets.QVBoxLayout()

        buttonHBox.addWidget(clipBtn)
        buttonHBox.addStretch()
        buttonHBox.addWidget(okBtn)

        mainVBox.addWidget(self.table)
        mainVBox.addLayout(buttonHBox)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(mainVBox)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(500,600)
        self.centerWindow()

    def getAppIcon(self):
        homeDir = os.path.dirname(__file__)
        return QtGui.QIcon(os.path.join(homeDir,"mediainfo.png"))

    def centerWindow(self):
        screen = QApplication.primaryScreen().geometry()
        frameGm = self.frameGeometry()
        frameGm.moveCenter(screen.center())
        self.move(frameGm.topLeft())

    def createListWidget(self):
        table = QtWidgets.QTableWidget()
        font = QFont()
        font.setPointSize(font.pointSize()-1)
        table.setFont(font)
        table.setColumnCount(2)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        table.setHorizontalHeaderLabels(["Item","Data"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        return table

    def fillTable(self, rows):
        self.rows = rows
        for row in rows:
            self.addTextLine(row)

    def addTextLine(self, strings):
        row= self.table.rowCount()
        self.table.insertRow(row)
        col=0
        is_header = isHeader(strings)
        for item in strings:
            qtitem = QtWidgets.QTableWidgetItem(item)
            if is_header:
                if col == 0:
                    font = QFont()
                    font.setBold(True)
                    qtitem.setFont(font)
                qtitem.setBackground(QtGui.QBrush(self.hdr_bg))
                qtitem.setForeground(QtGui.QBrush(self.hdr_fg))
            self.table.setItem(row,col,qtitem)
            col=col+1

    #  ------------ Callback section -----------------
    def callback_copy(self):
        QApplication.clipboard().setText(formatForClipboard(self.rows))

    def callback_btn_ok(self):
        QApplication.quit()


#desktops that are Qt based and theme us without help - same list as VideoCut
QT_DESKTOPS = ["kde","plasma","lxqtt","trinity desktop","lumina","lomiri","cutefish","ukui","thedesk","razor","deepin","dde"]


def main(argv = None):
    #force xcb: as a native wayland client Qt draws its own client side
    #decorations, which do not follow the window manager theme. Through xcb the
    #WM decorates the window and it matches the desktop. Must be set before the
    #QApplication is created (see VideoCut, OSTools.setGTKEnvironment)
    if os.environ.get("XDG_CURRENT_DESKTOP","").lower() not in QT_DESKTOPS:
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app=QApplication(sys.argv)
    #setWindowIcon only feeds _NET_WM_ICON, which does not exist on wayland -
    #there the icon comes from the .desktop named by setDesktopFileName
    app.setApplicationName("MediaInfoGui")
    app.setDesktopFileName("MediaInfoGui")
    view=MediaInfoView(argv[0])
    view.fillTable(argv[1])
    view.show()
    app.exec()

if __name__ == '__main__':
    sys.exit(main())
