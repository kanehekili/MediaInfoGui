# -*- coding: utf-8 -*-
'''
Created on Nov 18, 2011

@author: kanehekili
'''
import sys
import os
import gi
import locale
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk,GLib,Pango
from MediaInfoGui import isHeader, formatForClipboard

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

        
        #create the button bar
        btnBar = Gtk.HBox(homogeneous=False, spacing=0)
        buttonCopy = Gtk.Button(label="Clip")
        buttonCopy.connect("clicked", self.callback_copy)
        buttonOK = Gtk.Button(label="egal", stock=Gtk.STOCK_OK)
        buttonOK.connect("clicked", self.callback_btn_ok, "OK button")
        btnBar.pack_start(buttonCopy, False, False, 0)
        btnBar.pack_end(buttonOK, False, False, 0)
        layoutTable.attach(btnBar, 0, 2, 1, 2,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND,
            Gtk.AttachOptions.FILL, 1, 1)
        #layoutTable.set_row_spacing(row=0,spacing=5)
        self.window.add(layoutTable)
       
        self.window.show_all()
        sc = self.treeView.get_style_context()
        self.header_bg_rgba = sc.get_background_color(Gtk.StateFlags.SELECTED)
        self.header_fg_rgba = sc.get_color(Gtk.StateFlags.SELECTED)
    
    ##create a text view 
    def createTextWidget(self):
        self.treeView = Gtk.TreeView(model=self.createTreeStore())
        self.treeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        sel = self.treeView.get_selection()
        # every field (row) can be selected - Ctrl+C copies it (see _on_key_press)
        sel.set_mode(Gtk.SelectionMode.SINGLE)
        self.treeView.connect("key-press-event", self._on_key_press)
        
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
    
    def _headerCellData(self, column, renderer, model, iter, col_idx):
        is_header = isHeader((model.get_value(iter, 0), model.get_value(iter, 1)))
        if is_header:
            renderer.set_property('cell-background-rgba', self.header_bg_rgba)
            renderer.set_property('cell-background-set', True)
            renderer.set_property('foreground-rgba', self.header_fg_rgba)
            renderer.set_property('foreground-set', True)
            renderer.set_property('weight', 700)
        else:
            renderer.set_property('cell-background-set', False)
            renderer.set_property('foreground-set', False)
            renderer.set_property('weight', 400)

    def createColumn(self,columnContainer,headerString,columnID):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(headerString, rendererText, text=columnID)
        column.set_cell_data_func(rendererText, self._headerCellData, columnID)
        columnContainer.append_column(column)
 
    def fillTable(self, rows):
        for row in rows:
            self.addTextLine(row)

    #adds an array of strings. For the media view we need the Item name and value        
    def addTextLine(self, strings):
        self.store.append(strings)
        
    def openView(self):
        Gtk.main()
        #control returns if quit is called
        return 0;
    
    
    # Ctrl+C copies the selected field in the same format as the Clip button
    def _on_key_press(self, widget, event):
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval in (Gdk.KEY_c, Gdk.KEY_C):
            model, tree_paths = self.treeView.get_selection().get_selected_rows()
            if tree_paths:
                iters = [model.get_iter(p) for p in tree_paths]
                rows = [(model.get_value(it, 0), model.get_value(it, 1)) for it in iters]
                clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
                clipboard.set_text(formatForClipboard(rows), -1)
                clipboard.store()
            return True
        return False

    #  ------------ Callback section -----------------
    def callback_copy(self, widget, data=None):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(formatForClipboard([(r[0], r[1]) for r in self.store]), -1)
        clipboard.store()

    def callback_btn_ok(self, widget, data=None):
        Gtk.main_quit();
    
    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False    
   

def main(argv = None):
    if argv is None:
        argv = sys.argv

    view=MediaInfoView(argv[0])
    view.fillTable(argv[1])
    view.openView()
    

if __name__ == '__main__':
    sys.exit(main())

