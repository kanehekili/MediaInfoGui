# -*- coding: utf-8 -*-
'''
Created on May 01 2020

@author: kanehekili
'''
import sys
import re
import os
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QErrorMessage
from PyQt5.Qt import QMainWindow, QSizePolicy, QFont

class MediaInfoView(QMainWindow):
    
    def __init__(self,fileName):
        super(MediaInfoView,self).__init__()
        self.initUI(fileName)
        
    def initUI(self,fileName):
        self.setWindowTitle(fileName)
        
        #the icon
        self.setWindowIcon(self.getAppIcon())
        
#         frame = QtWidgets.QFrame()
#         #need qGroupBox for title....
#         frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
#         frame.setLineWidth(1)
#         frame.setMidLineWidth(0)
#         frame.setStyleSheet(".QFrame{border: 1px solid gray; border-radius: 6px;}")
        ##round and "Media Info Text
        self.table = self.createListWidget()
        buttonBox=QtWidgets.QDialogButtonBox(self)
        okbtn = buttonBox.addButton(QtWidgets.QDialogButtonBox.Ok)
        okbtn.clicked.connect(self.callback_btn_ok)
        
        buttonHBox = QtWidgets.QHBoxLayout();
        mainVBox = QtWidgets.QVBoxLayout();
        
        buttonHBox.addWidget(buttonBox)
        
        mainVBox.addWidget(self.table)
        mainVBox.addLayout(buttonHBox)
        #1frame.setLayout(mainVBox)
        #1fullVBox.addWidget(frame)
        
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        #1wid.setLayout(fullVBox)
        wid.setLayout(mainVBox)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.setMinimumSize(500,600)
        self.centerWindow()
    
    def getAppIcon(self):
        homeDir = os.path.dirname(__file__)
        return QtGui.QIcon(os.path.join(homeDir,"mediainfo.png"))

    def centerWindow(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    ##create a text view 
    def createListWidget(self):
        table = QtWidgets.QTableWidget()
        font = QFont()
        font.setPointSize(font.pointSize()-1)
        table.setFont(font)
        table.setColumnCount(2)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded);
        table.setHorizontalHeaderLabels(["Item","Data"])
        header= table.horizontalHeader()
        #ok, with gap header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # works, but initially too small: header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        #ok, but then no scrollbar: header.setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setStretchLastSection(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        return table
       

    def fillTable(self,mediaInfoList):
        for line in mediaInfoList:
            row = line.decode("utf-8")
            token=re.split('[ ]+:[ ]+',row)
            if len(token) == 1:
                data=(token[0],"")
            else:
                data=(token[0],token[1])     
            self.addTextLine(data)
    

    #adds an array of strings. For the media view we need the Item name and value        
    def addTextLine(self, strings):
        row= self.table.rowCount()
        self.table.insertRow(row)
        col=0
        setFont=False
        if len(strings[1]) == 0 and len(strings[0]) > 0:
            setFont=True
        for item in strings:
            qtitem = QtWidgets.QTableWidgetItem(item)
            if col == 0 and setFont:
                font = QFont()
                font.setBold(True)
                qtitem.setFont(font)
            self.table.setItem(row,col,qtitem)
            col=col+1
    
    #  ------------ Callback section -----------------
    # The data passed to this method is printed to stdout
    def callback_btn_ok(self, index):
        QApplication.quit()
   
   

def showMessage(messageString):
    app = QtWidgets.QApplication([])
    msg = QErrorMessage()
    msg.showMessage(messageString)
    app.exec()
    #simple error dialog
    
   


def main(argv = None):
    app=QApplication(sys.argv)
    view=MediaInfoView(argv[0])
    view.fillTable(argv[1])
    view.show()
    
    app.exec()

if __name__ == '__main__':
    sys.exit(main())

