sudo apt update
sudo apt install samba dosfstools mtools watchdog python3-watchdog -y

echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules

