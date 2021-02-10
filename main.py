import gi
import os
import subprocess

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

class PaInstaller(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Paranoid Installer")
        self.set_border_width(10)
        hbox = Gtk.Box(spacing=6)
        self.add(hbox)
        self.aboutDevice = Gtk.Button(label='Check Connected Device')
        self.aboutDevice.connect("clicked", self.on_about_device)
        hbox.pack_start(self.aboutDevice, True, True, 0)
        self.button = Gtk.Button(label='Reboot to Fastboot')
        self.button2 = Gtk.Button(label='Move to ADB shell')
        self.button.connect("clicked", self.on_pa_click)
        hbox.pack_start(self.button, True, True, 0)
        self.button2.connect("clicked", self.on_pa_adb)
        hbox.pack_start(self.button2, True, True, 0)

    def on_about_device(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Connected device",
        )
        dialog.format_secondary_text(
            "Connected device: "+getDeviceCodename()
        )
        dialog.run()
        print("Task dialog closed")

        dialog.destroy()


    def Finished(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Task completed successfully",
        )
        dialog.format_secondary_text(
            "The given task completed successfully."
        )
        dialog.run()
        print("Task dialog closed")

        dialog.destroy()

    def on_pa_click(self, widget):
        os.system('adb reboot bootloader')
        dialog = self.Finished(self)

    def on_pa_adb(self, widget):
        os.system('adb shell')
        dialog = self.Finished(self)

win = PaInstaller()
win.connect("destroy",Gtk.main_quit)

win.show_all()
Gtk.main()
