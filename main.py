#!/usr/bin/python3

import gi
import subprocess
import time
import os

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

def isAbDevice():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.boot.slot_suffix"'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip() is not None

def get_adb(parent, message, title=''):
    dialogWindow = Gtk.MessageDialog(parent,
                      Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                      Gtk.MessageType.QUESTION,
                      Gtk.ButtonsType.OK_CANCEL,
                      message)
    dialogWindow.set_title(title)
    dialogWindow.set_border_width(10)
    dialogBox = dialogWindow.get_content_area()
    userEntry = Gtk.Entry()
    userEntry.set_visibility(True)
    userEntry.set_size_request(250,0)
    dialogBox.pack_end(userEntry, False, False, 0)
    dialogWindow.show_all()
    response = dialogWindow.run()
    text = userEntry.get_text() 
    dialogWindow.destroy()
    if (response == Gtk.ResponseType.OK) and (text != ''):
        return text
    else:
        return None    
        
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
        self.romFlashSideload = Gtk.Button(label='Flash a ZIP using sideload')
        self.romFlashSideload.connect("clicked", self.on_rom_adb_flash)
        hbox.pack_start(self.romFlashSideload, True, True, 0)
        self.romFlashFboot = Gtk.Button(label='Flash a ZIP using fastboot')
        self.romFlashFboot.connect("clicked", self.on_rom_flash_fboot)
        hbox.pack_start(self.romFlashFboot, True, True, 0)
        self.imgFlashFboot = Gtk.Button(label='Flash an image using fastboot')
        self.imgFlashFboot.connect("clicked", self.fastbootflashsep)
        hbox.pack_start(self.imgFlashFboot, True, True, 0)
        self.dataWipe = Gtk.Button(label='Wipe userdata')
        self.dataWipe.connect("clicked", self.on_data_wipe)
        hbox.pack_start(self.dataWipe, True, True, 0)
        self.sendPowerKeycode = Gtk.Button(label='Turn on/off display')
        self.sendPowerKeycode.connect("clicked", self.on_keycode_power)
        hbox.pack_start(self.sendPowerKeycode, True, True, 0)
        self.sendScreencast = Gtk.Button(label='Cast screen of connected device')
        self.sendScreencast.connect("clicked", self.on_screencast)
        hbox.pack_start(self.sendScreencast, True, True, 0)
        self.connectWlanADB = Gtk.Button(label='Connect via ADB to device wirelessly')
        self.connectWlanADB.connect("clicked", self.on_adb_wlan_connect)
        hbox.pack_start(self.connectWlanADB, True, True, 0)
        self.disconnectAll = Gtk.Button(label="Disconnect all wirelessly connected devices")
        self.disconnectAll.connect("clicked", self.on_all_disconnect)
        hbox.pack_start(self.disconnectAll, True, True, 0)
        self.appInstall = Gtk.Button(label="Install apps via ADB")
        self.appInstall.connect("clicked", self.on_app_install)
        hbox.pack_start(self.appInstall, True, True, 0)
        self.getLogcat = Gtk.Button(label="Get logcat via ADB")
        self.getLogcat.connect("clicked", self.on_get_logcat)
        hbox.pack_start(self.getLogcat, True, True, 0)

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

    def on_all_disconnect(self, widget):
        subprocess.run(['adb','disconnect'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_fastboot_click(self, widget):
        subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_recovery_reboot(self, widget):
        subprocess.run(['adb', 'reboot', 'recovery'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_keycode_power(self, widget):
        subprocess.run(['adb','shell','input','keyevent','KEYCODE_POWER'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)
    
    def on_screencast(self,widget):
        os.system('adb shell screenrecord --output-format=h264 - | ffplay -framerate 60 -probesize 32 -sync video - & watch -n 1 "pgrep ffplay || pkill -f \'adb shell\' "')
        dialog = self.Finished(self)
        
    def on_adb_wlan_connect(self,widget):
        deviceIP = get_adb(self, "Please enter the IP address along with the port", "Connect to ADB via WiFi")
        subprocess.run(['adb','connect',deviceIP], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_get_logcat(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Getting a logcat via ADB",
        )
        dialog.format_secondary_text(
            "The log will be saved in a file called logcat.txt in the same directory that CSAK is stored in. The script might hang because it is a continuous process with no end, so in order to stop capturing logs, Ctrl+C in the terminal window that you used to start CSAK."
        )
        dialog.run()
        os.system('adb logcat > logcat.txt')
        print("Task dialog closed")

        dialog.destroy()


    def fastbootflashsep(self,widget):
        devicepart = get_adb(self, "Please enter the partition you want to flash to (case-sensitive)", "Flash image")
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
        subprocess.run(['fastboot','flash',devicepart,final], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def add_filters_app(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("APK files")
        filter_text.add_mime_type("application/vnd.android.package-archive")
        dialog.add_filter(filter_text)

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
            subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            time.sleep(10)
            if isAbDevice():
                recovery_partition = 'boot'
            else:
                recovery_partition = 'recovery'
            subprocess.run(['fastboot','flash',recovery_partition,final], stdout=subprocess.PIPE).stdout.decode('utf-8')
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def add_filters_rom(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("ZIP files")
        filter_text.add_mime_type("application/zip")
        dialog.add_filter(filter_text)

    def on_data_wipe(self, dialog):
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
            subprocess.run(['adb','reboot','bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            time.sleep(10)
            subprocess.run(['fastboot','erase','userdata'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            time.sleep(10)
            subprocess.run(['fastboot','reboot','recovery'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Task completed successfully",
            )
            dialog.format_secondary_text(
                "Your phone should auto reboot to recovery in a few seconds. If it doesn't, reboot forcefully after the process on your device has completed, or if it bootloops, try to flash the correct package and try again."
            )
            dialog.run()
            print("INFO dialog closed")

            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def on_rom_flash_fboot(self, dialog):
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
            subprocess.run(['adb','reboot','bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            time.sleep(10)
            subprocess.run(['fastboot','update',final], stdout=subprocess.PIPE).stdout.decode('utf-8')
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Task completed successfully",
            )
            dialog.format_secondary_text(
                "Successfully flashed zip via fastboot."
            )
            dialog.run()
            print("INFO dialog closed")

            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def on_rom_adb_flash(self, dialog):
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
            subprocess.run(['adb','reboot','sideload-auto-reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
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

    def on_app_install(self, dialog):
        dialog = Gtk.FileChooserDialog(
            title="Please choose an APK file to install", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters_app(dialog)

        response = dialog.run()
        final = ""
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            final = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
        subprocess.run(['adb','install',final], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)


win = GMInstaller()
win.connect("destroy",Gtk.main_quit)

win.show_all()
Gtk.main()
