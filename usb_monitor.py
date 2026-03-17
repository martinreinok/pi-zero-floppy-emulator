import time
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATH = "/mnt/cnc_disks"
CMD_RELOAD = "sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' && sudo modprobe -r g_mass_storage && sleep 1 && sudo modprobe g_mass_storage file=/home/pizerocnc2/original_cnc_image.bin stall=0 ro=1 removable=1"

class RefreshUSB(FileSystemEventHandler):
    def __init__(self):
        self.timer = None
        self.cooldown = 3.0  # Wait 3 seconds AFTER file finishes transferring

    def reload_usb(self):
        print("Transfer complete. Executing USB reload sequence...")
        subprocess.call(CMD_RELOAD, shell=True)

    def process_event(self, event):
        if event.is_directory:
            return

        # Ignore macOS hidden system files
        if ".DS_Store" in event.src_path or "/._" in event.src_path:
            return

        # Only react to actual file changes, not just "reads"
        if event.event_type in ['modified', 'created', 'deleted', 'moved']:
            print(f"[{time.strftime('%H:%M:%S')}] Detected {event.event_type} on: {event.src_path}")

            # Cancel the old timer and start a new one (Debounce)
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.cooldown, self.reload_usb)
            self.timer.start()

    def on_created(self, event): self.process_event(event)
    def on_modified(self, event): self.process_event(event)
    def on_deleted(self, event): self.process_event(event)
    def on_moved(self, event): self.process_event(event)

observer = Observer()
observer.schedule(RefreshUSB(), WATCH_PATH, recursive=True)
observer.start()

print("CNC USB Watchdog started")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

