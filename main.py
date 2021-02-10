import gi
import os

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

class PaInstaller(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Paranoid Installer")
        grid = Gtk.Grid()
        self.add(grid)
        self.button = Gtk.Button(label='Reboot to Fastboot')
        self.button2 = Gtk.Button(label='Move to ADB shell')
        self.button.connect("clicked", self.on_pa_click)
        self.button2.connect("clicked", self.on_pa_adb)
        grid.add(self.button)
        grid.attach(self.button2, 1,0,2,1)

    def on_pa_click(self, widget):
        os.system('adb reboot bootloader')
        
    def on_pa_adb(self, widget):
        os.system('adb shell')

win = PaInstaller()
win.connect("destroy",Gtk.main_quit)

win.show_all()
Gtk.main()
