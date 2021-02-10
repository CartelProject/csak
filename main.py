import gi
import subprocess
import time

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

class GMInstaller(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Cartel Swiss Army Knife")
        self.set_border_width(10)
        hbox = Gtk.Box(spacing=6)
        hbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(hbox)
        self.aboutDevice = Gtk.Button(label='Check Connected Device')
        self.aboutDevice.connect("clicked", self.on_about_device)
        hbox.pack_start(self.aboutDevice, True, True, 0)
        self.recoveryreboot = Gtk.Button(label='Reboot to Recovery')
        self.recoveryreboot.connect("clicked", self.on_recovery_reboot)
        hbox.pack_start(self.recoveryreboot, True, True, 0)
        self.fastbootreboot = Gtk.Button(label='Reboot to Fastboot')
        self.fastbootreboot.connect("clicked", self.on_fastboot_click)
        hbox.pack_start(self.fastbootreboot, True, True, 0)
        self.recoveryFlash = Gtk.Button(label='Flash a recovery image')
        self.recoveryFlash.connect("clicked", self.on_recovery_flash)
        hbox.pack_start(self.recoveryFlash, True, True, 0)
        self.romFlash = Gtk.Button(label='Flash a ROM using sideload')
        self.romFlash.connect("clicked", self.on_rom_flash)
        hbox.pack_start(self.romFlash, True, True, 0)

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

    def on_fastboot_click(self, widget):
        subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_recovery_reboot(self, widget):
        subprocess.run(['adb', 'reboot', 'recovery'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def add_filters_recovery(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Recovery images")
        filter_text.add_mime_type("application/x-raw-disk-image")
        dialog.add_filter(filter_text)

    def on_recovery_flash(self, dialog):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters_recovery(dialog)

        response = dialog.run()
        final = ""
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            final = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Caution",
        )
        dialog.format_secondary_text(
            "The changes made are irreversible! Do you want to continue?"
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("WARN dialog closed by clicking OK button")
            print(final)
            subprocess.run(['fastboot','flash','recovery',final], stdout=subprocess.PIPE).stdout.decode('utf-8')
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def add_filters_rom(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("ZIP files")
        filter_text.add_mime_type("application/zip")
        dialog.add_filter(filter_text)

    def on_rom_flash(self, dialog):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters_rom(dialog)

        response = dialog.run()
        final = ""
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            final = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Caution",
        )
        dialog.format_secondary_text(
            "The changes made are irreversible! Do you want to continue?"
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("WARN dialog closed by clicking OK button")
            print(final)
            subprocess.run(['adb','reboot','sideload-auto-reboot',final], stdout=subprocess.PIPE).stdout.decode('utf-8')
            time.sleep(10)
            subprocess.run(['adb','sideload',final], stdout=subprocess.PIPE).stdout.decode('utf-8')
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Task completed successfully",
            )
            dialog.format_secondary_text(
                "Your phone should auto reboot to system in a few seconds. If it doesn't, reboot forcefully after the process on your device has completed, or if it bootloops, try to flash the correct package and try again."
            )
            dialog.run()
            print("INFO dialog closed")

            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()


win = GMInstaller()
win.connect("destroy",Gtk.main_quit)

win.show_all()
Gtk.main()
