#!/usr/bin/env python3
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: sudo python3 clone_existing_usb.py /dev/sdX")

drive, image_file = sys.argv[1], "/home/pizerocnc/original_cnc_image.bin"
offsets = []

print(f"[*] Cloning {drive} to {image_file} (256MB)...")
try:
    with open(drive, 'rb') as f_in, open(image_file, 'wb') as f_out:
        for _ in range(256):
            f_out.write(f_in.read(1024 * 1024))
            print(".", end="", flush=True)
except Exception as e:
    sys.exit(f"\n[!] Clone failed: {e}")

print(f"\n[*] Scanning {image_file} for FAT12 boot sectors...")
with open(image_file, 'rb') as f:
    offset = 0
    while chunk := f.read(512):
        if len(chunk) >= 62 and chunk[54:62] == b'FAT12   ':
            offsets.append(offset)
        offset += 512

print(f"\n[+] Found {len(offsets)} virtual floppies.")
if len(offsets) > 1:
    print(f"[+] Distance between disks: {offsets[1] - offsets[0]} bytes.")
    for i in range(min(3, len(offsets))):
        print(f"    Disk {i:03d} starts at byte: {offsets[i]}")
