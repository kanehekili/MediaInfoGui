# -*- coding: utf-8 -*-
'''
Created on 2025

@author: kanehekili
'''
import sys
import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango
from MediaInfoGui import isHeader, formatForClipboard


class MediaInfoView(Gtk.ApplicationWindow):

    def __init__(self, app, fileName):
        super().__init__(application=app, title=fileName)
        self.set_default_size(500, 600)

        # Fallback header colours — overridden once the widget is realized
        self.header_bg_rgba = Gdk.RGBA()
        self.header_bg_rgba.parse("#3584e4")
        self.header_fg_rgba = Gdk.RGBA()
        self.header_fg_rgba.parse("#ffffff")
        self.connect("realize", self._on_realize)

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        outer.set_margin_start(5)
        outer.set_margin_end(5)
        outer.set_margin_top(5)
        outer.set_margin_bottom(5)

        frame = Gtk.Frame(label="Media Info")
        frame.set_vexpand(True)
        frame.set_child(self._buildTreeView())
        outer.append(frame)

        btn_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        clip_btn = Gtk.Button(label="Clip")
        clip_btn.connect("clicked", self._on_clip)
        ok_btn = Gtk.Button(label="OK")
        ok_btn.connect("clicked", self._on_ok)
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        btn_bar.append(clip_btn)
        btn_bar.append(spacer)
        btn_bar.append(ok_btn)
        outer.append(btn_bar)

        self.set_child(outer)

    def _on_realize(self, widget):
        sc = self.treeView.get_style_context()
        found_bg, bg = sc.lookup_color("theme_selected_bg_color")
        found_fg, fg = sc.lookup_color("theme_selected_fg_color")
        if found_bg:
            self.header_bg_rgba = bg
        if found_fg:
            self.header_fg_rgba = fg
        self.treeView.queue_draw()

    def _buildTreeView(self):
        self.store = Gtk.ListStore(str, str)
        self.treeView = Gtk.TreeView(model=self.store)
        self.treeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        # every field (row) can be selected - Ctrl+C copies it (see _on_key_pressed)
        self.treeView.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        # GTK4 has no key-press-event signal - use a key event controller
        keyCtrl = Gtk.EventControllerKey()
        keyCtrl.connect("key-pressed", self._on_key_pressed)
        self.treeView.add_controller(keyCtrl)
        self._addColumn("Item", 0)
        self._addColumn("Data", 1)
        sw = Gtk.ScrolledWindow()
        sw.set_child(self.treeView)
        sw.set_vexpand(True)
        return sw

    def _addColumn(self, header, col_id):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(header, renderer, text=col_id)
        column.set_cell_data_func(renderer, self._headerCellData, col_id)
        self.treeView.append_column(column)

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

    def fillTable(self, rows):
        for row in rows:
            self.store.append(row)

    # Ctrl+C copies the selected field in the same format as the Clip button
    def _on_key_pressed(self, controller, keyval, keycode, state):
        if state & Gdk.ModifierType.CONTROL_MASK and keyval in (Gdk.KEY_c, Gdk.KEY_C):
            model, tree_paths = self.treeView.get_selection().get_selected_rows()
            if tree_paths:
                iters = [model.get_iter(p) for p in tree_paths]
                rows = [(model.get_value(it, 0), model.get_value(it, 1)) for it in iters]
                provider = Gdk.ContentProvider.new_for_bytes(
                    "text/plain;charset=utf-8",
                    GLib.Bytes.new(formatForClipboard(rows).encode("utf-8"))
                )
                self.get_clipboard().set_content(provider)
            return True
        return False

    def _on_clip(self, widget):
        text = formatForClipboard([(r[0], r[1]) for r in self.store])
        provider = Gdk.ContentProvider.new_for_bytes(
            "text/plain;charset=utf-8",
            GLib.Bytes.new(text.encode("utf-8"))
        )
        self.get_clipboard().set_content(provider)

    def _on_ok(self, widget):
        self.get_application().quit()


def main(argv=None):
    app = Gtk.Application()

    def on_activate(application):
        win = MediaInfoView(application, argv[0])
        win.fillTable(argv[1])
        win.present()

    app.connect("activate", on_activate)
    app.run(None)


if __name__ == '__main__':
    sys.exit(main())
