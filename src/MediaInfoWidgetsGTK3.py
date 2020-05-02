'''
Created on Nov 18, 2011

@author: kanehekili
'''
import sys,re
import os
import gi
import locale
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk,GLib,Pango

class MediaInfoView:
    
    def __init__(self,fileName):
    #create Window
        self.window = Gtk.Window()
        #set the window Title
        self.window.set_title(fileName)
        #the icon
        homeDir = os.path.dirname(__file__)
        appIcon = os.path.join(homeDir,"mediainfo.png")
        self.window.set_icon_from_file(appIcon)
        self.window.connect("delete_event",self.delete_event)
        self.window.set_border_width(5)
        self.window.set_size_request(500,600)
        #create some kind of layout in which the widgets are packed
        #layoutTable = gtk.Table(rows=2,columns=2,True)
        layoutTable = Gtk.Table(rows=2,columns=2,homogeneous=False)
        #TODO use buttonbox for buttons....
        
        #create a widget the could contain the data
        infoFrame=Gtk.Frame()
        infoFrame.set_label("Media Info")
        infoFrame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        

        sw = self.createTextWidget()   
        sw.set_border_width(5)     
        vbox = Gtk.VBox(homogeneous=False, spacing=0)
        vbox.pack_start(sw, expand=True, fill=True, padding=0)
        hbox = Gtk.HBox(homogeneous=False, spacing=0)
        hbox.pack_start(vbox, expand=True, fill=True, padding=1)
        
        infoFrame.add(hbox)

        layoutTable.attach(infoFrame,0,2,0,1,Gtk.AttachOptions.FILL| Gtk.AttachOptions.EXPAND,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, 1, 1)

        
        #create the ok button that closes all
        dummy = Gtk.Label()
        buttonOK = Gtk.Button(label="egal",stock=Gtk.STOCK_OK)
        buttonOK.set_size_request(100, 40)
        buttonOK.connect("clicked",self.callback_btn_ok,"OK button")
        layoutTable.attach(buttonOK,1,2,1,2,Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.FILL)
        
        layoutTable.attach(dummy,0,1,1,2,Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.FILL)
        #layoutTable.set_row_spacing(row=0,spacing=5)
        self.window.add(layoutTable)
       
        self.window.show_all()
    
    ##create a text view 
    def createTextWidget(self):
        self.treeView = Gtk.TreeView(model=self.createTreeStore())
        self.treeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        sel = self.treeView.get_selection()
        sel.set_mode(Gtk.SelectionMode.NONE)
        
        #fontName="Monospace 9"
        fontName=""
        pangoFont = Pango.FontDescription(fontName)
        self.treeView.modify_font(pangoFont)
        self.createColumn(self.treeView, "Item",0)
        self.createColumn(self.treeView, "Data",1)
        
        sw = Gtk.ScrolledWindow()
        #sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        sw.add(self.treeView)
        return sw
       
    def createTreeStore(self):
        self.store = Gtk.ListStore(str,str)
        return self.store
    
    def createColumn(self,columnContainer,headerString,columnID):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(headerString, rendererText, text=columnID)
        #column.set_sort_column_id(columnID)    
        columnContainer.append_column(column)
 
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
        self.store.append(strings)
        
    def openView(self):
        Gtk.main()
        #control returns if quit is called
        return 0;
    
    
    #  ------------ Callback section -----------------
    # The data passed to this method is printed to stdout
  
    def callback_btn_ok(self, widget, data=None):
        Gtk.main_quit();
    
    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False    
   

def showMessage(messageString):
    message = Gtk.MessageDialog(None,
                             Gtk.DialogFlags.MODAL,
                             Gtk.MessageType.INFO,
                             Gtk.ButtonsType.NONE,
                             messageString)
    message.add_button(Gtk.STOCK_QUIT, Gtk.ResponseType.CLOSE)
    resp = message.run()
    closewidget(message)

#hook to ensure closing widget
def closewidget(widget):
    widget.destroy()
    while Gtk.events_pending():
        Gtk.main_iteration()
     
         

def main(argv = None):
    if argv is None:
        argv = sys.argv

    view=MediaInfoView(argv[0])
    view.fillTable(argv[1])
    view.openView()
    

if __name__ == '__main__':
    sys.exit(main())

