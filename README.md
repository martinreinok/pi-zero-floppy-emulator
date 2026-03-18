# Floppy USB emulator
Make a PI Zero 2W into a USB stick that emulates USB-floppy, for an industrial controller.

## Research
https://github.com/rocketcrane/Pi-Floppy

https://magazine.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive

## Samba config

nano /etc/samba/smb.conf
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

Add samba user
```
sudo smbpasswd -a pizerocnc2
sudo smbpasswd -e pizerocnc2
```

sudo systemctl restart smbd

## Wifi config
nmcli device wifi list

nmcli device wifi connect "ssid" password "pw"

nmcli connection up "ssid"

nmcli connection delete "ssid"

add wifi which is not present yet:
```
sudo nmcli connection add type wifi ifname wlan0 con-name "SSID" ssid "SSID"
sudo nmcli connection modify "SSID" wifi-sec.key-mgmt sae
sudo nmcli connection modify "SSID" wifi-sec.psk "PASSWORD_HERE"
sudo nmcli connection modify "SSID" connection.autoconnect yes
```


### Turn off power saving mode!
```
sudo mkdir -p /etc/NetworkManager/conf.d
printf "[connection]\nwifi.powersave = 2\n" | sudo tee /etc/NetworkManager/conf.d/wifi-powersave.conf
```

### Manual IP
```
sudo nmcli connection modify "SSID" ipv4.addresses 192.168.1.6/24 ipv4.gateway 192.168.1.1 ipv4.dns "1.1.1.1 8.8.8.8" ipv4.method manual
sudo reboot
```

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
ExecStart=/usr/bin/python3 /home/pizerocnc/cnc-usb-emulator/usb_monitor.py
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

## Hardening
```
systemctl list-unit-files --type=service --state=enabled
systemctl disable bluetooth
sudo apt purge gcc make gdb
sudo systemctl disable --now bluetooth
sudo systemctl disable --now cloud-config cloud-final cloud-init-local cloud-init-main cloud-init-network
systemctl list-unit-files --type=service
sudo systemctl disable getty@tty1
sudo systemctl disable --now keyboard-setup console-setup
sudo systemctl disable --now udisks2
sudo systemctl disable ModemManager.service
sudo systemctl disable regenerate_ssh_host_keys.service
```

ssh only key auth
