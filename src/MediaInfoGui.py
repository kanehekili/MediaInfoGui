# -*- coding: iso-8859-15 -*-
'''
Created on Nov 25, 2011
Vernünftige GTK Oberfläche für media info
@author: kanehekili
'''
import subprocess
import sys
from subprocess import Popen



VERSION="@xxxx@"


def readMediaInfo(type,filename):
    nameValid=False
    if len(filename)>3:
        result=Popen(["mediainfo",filename],stdout=subprocess.PIPE).communicate()[0]
        nameValid= len(result) > 10
        
    if not nameValid:
        if type == "gtk3":
            import MediaInfoWidgetsGTK3
            MediaInfoWidgetsGTK3.showMessage("Invalid File for Media Info")
        else:
            import MediaInfoWidgetsQt     
            MediaInfoWidgetsQt.showMessage("Invalid File for Media Info")
        return 0
    showListDialog(type,filename,result.splitlines())


def showListDialog(type,fileName,mediaInfoList):
    paths = fileName.split("/")
    pLen = len(paths)
    item = paths[pLen-2]+"/"+paths[pLen-1]
    if type == "gtk3":
        import MediaInfoWidgetsGTK3        
        MediaInfoWidgetsGTK3.main([item,mediaInfoList])
    else:
        import MediaInfoWidgetsQt  
        MediaInfoWidgetsQt.main([item,mediaInfoList])
    

def main(argv = None):
    filename=""
    type=""
    if argv is None:
        argv = sys.argv
        if len(argv)>1:
            type=argv[1]
        if len(argv)>2:            
            filename=argv[2]
            

    print("Version:"+VERSION)
    readMediaInfo(type,filename)
    
if __name__ == '__main__':
    sys.exit(main())    