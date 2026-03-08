# Floppy USB emulator
Make a PI Zero 2W into a USB stick that emulates USB-floppy, for an industrial controller.

## Research
https://github.com/rocketcrane/Pi-Floppy

https://magazine.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive

## Samba config

```
[CNC_Floppy]
   path = /mnt/cnc_disks
   browseable = yes
   guest ok = no
   read only = no
   valid users = pizerocnc
   create mask = 0770
   directory mask = 0770
```

sudo systemctl restart smbd

## Wifi config
nmcli device wifi list

nmcli device wifi connect "ssid" password "pw"

nmcli connection up "ssid"

nmcli connection delete "ssid"

## systemctl config

sudo nano /etc/systemd/system/cnc_emulator.service
```
[Unit]
Description=CNC Floppy USB Emulator
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash /home/pizerocnc/cnc-usb-emulator/start_cnc_usb.sh
WorkingDirectory=/home/pizerocnc/cnc-usb-emulator
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

sudo nano /etc/systemd/system/cnc_watchdog.service
```
[Unit]
Description=CNC Floppy USB Watchdog
Requires=cnc_emulator.service
After=cnc_emulator.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pizerocnc/cnc-usb-emulator/watchdog.py
WorkingDirectory=/home/pizerocnc/cnc-usb-emulator
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload
sudo systemctl enable cnc_emulator.service
sudo systemctl enable cnc_watchdog.service

sudo systemctl start cnc_watchdog.service
