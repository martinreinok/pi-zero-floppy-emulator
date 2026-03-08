# Floppy USB emulator
Make a PI Zero 2W into a USB stick that emulates USB-floppy, for an industrial controller.

## Research
https://github.com/rocketcrane/Pi-Floppy

https://magazine.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive

## Samba config

'''
[CNC_Floppies]
   path = /mnt/cnc_disks
   browseable = yes
   guest ok = yes
   read only = no
   create mask = 0777
'''

sudo systemctl restart smbd

## Wifi config
nmcli device wifi list

nmcli device wifi connect "ssid" password "pw"

nmcli connection up "ssid"

nmcli connection delete "ssid"
