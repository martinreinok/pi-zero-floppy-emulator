import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATH = "/mnt/cnc_disks"
CMD_RELOAD = "modprobe -r g_mass_storage && sleep 1 && modprobe g_mass_storage file=/home/pi/original_cnc_image.bin stall=0 ro=1 removable=1"

class RefreshUSB(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            print(f"File changed: {event.src_path}. Refreshing CNC USB...")
            # Brief delay to ensure file copy is finished over Samba
            time.sleep(2) 
            subprocess.call(CMD_RELOAD, shell=True)

observer = Observer()
observer.schedule(RefreshUSB(), WATCH_PATH, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

