![CSAK](/assets/banner.jpg)
#### An easy-to-use, plug-and-play device management script for Android devices.
Language: Python 3.8.x <br>
Platform: Linux/macOS with GTK 3.0 installed

```
/*
 * I'm not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because the alarm app failed. 
 * Please do some research if you have any concerns about features included in the products you find here before flashing it! 
 * YOU are choosing to make these modifications, and if you point the finger at me for messing up your device, I will laugh at you. 
 * Your warranty will be void if you tamper with any part of your device / software.
 */
```

### Installation and Running:
- Clone this repository to your desired location.
``` 
git clone https://github.com/CartelProject/csak csak
```
- Install Android SDK tools on Linux. A simple Google search can help you out.
- Install gi package or gtk 3.0 if you haven't yet
- For macOS users, to install gtk 3.0
```
brew install pygobject3 gtk+3
```
- If you have not installed Python yet, install Python 3.8.x or above on your PC.
- Run the following command to run the Python+GTK3.0 script:
```
python3 csak/main.py
```

### Features:
- ROMs, ZIP installer (works with any recovery that supports ADB sideload)
- Easy recovery installer
- Userdata wipe
- Detection of connected device (codename detection)
- Reboot to recovery and fastboot using one click
- Toggling device display on or off depending on phone state for phones with a broken power button
- Connect to ADB via WiFi
- Disconnect all WiFi ADB connected devices 
- Now screencast your phone's display onto your laptop easily
- Install apps via ADB
- Install compatible fastboot updatable zips. DO NOT CONFUSE THIS WITH THE NORMAL RECOVERY ZIPS THAT YOU GET!

### Screenshot:
![CSAK](/assets/screenshot.png)

### Known Issues:
- Screencast hangs after you close ffplay window
```
WORKAROUND
- Ctrl+C in terminal window after you have closed ffplay window
```

### In The Future
- Will add support for fastboot flashing IMGs for system, vendor, odm and other partitions respectively.
- Fix a bug where the script hangs due to process not completeing in time. Do not worry, if it hangs, DO NOT CANCEL THE SCRIPT OR FORCE CLOSE, OR IT MIGHT BRICK YOUR DEVICE IN THE PROCESS. Let the script complete, and check the terminal for progress.
- Will add support for automatic TWRP downloading and flashing depending on the codename

##### If you like my work, please consider donating!
###### Support email: malvi@aospa.co
