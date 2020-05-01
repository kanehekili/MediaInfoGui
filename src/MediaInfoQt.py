# -*- coding: iso-8859-15 -*-
'''
Created on Nov 25, 2011
Vernünftige GTK Oberfläche für media info
@author: kanehekili
'''
import subprocess
import sys
from subprocess import Popen
import MediaInfoWidgets

def readMediaInfo(filename):
    nameValid=False
    if len(filename)>3:
        result=Popen(["mediainfo",filename],stdout=subprocess.PIPE).communicate()[0]
        nameValid= len(result) > 10
        
    if not nameValid:
        MediaInfoWidgets.showMessage("Invalid File for Media Info")
        return 0
    showListDialog(filename,result.splitlines())


def showListDialog(fileName,mediaInfoList):
    paths = fileName.split("/")
    pLen = len(paths)
    item = paths[pLen-2]+"/"+paths[pLen-1]
    MediaInfoWidgets.main([item,mediaInfoList])
    

def main(argv = None):
    filename=""
    if argv is None:
        argv = sys.argv
        if len(argv)>1:
            filename=argv[1]

    readMediaInfo(filename)
    
if __name__ == '__main__':
    sys.exit(main())    