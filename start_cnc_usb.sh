#!/bin/bash

BIN_FILE="/home/pi/original_cnc_image.bin"  # Original cloned image
MOUNT_BASE="/mnt/cnc_disks"
NUM_DISKS=127
BLOCK_BYTES=1507328    # Distance between disks
START_OFFSET=512       # Disk 000 starts at byte

cleanup() {
    echo -e "\n[!] Shutting down CNC Emulation..."
    sudo modprobe -r g_mass_storage
    for i in $(seq 0 $NUM_DISKS); do
        DIR_NAME=$(printf "%03d" $i)
        sudo umount "${MOUNT_BASE}/Disk_${DIR_NAME}" 2>/dev/null
    done
    echo "[+] System restored."
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "[+] Mounting 127 internal FAT12 structures from Golden Image..."
mkdir -p $MOUNT_BASE
for i in $(seq 0 $NUM_DISKS); do
    DIR_NAME=$(printf "%03d" $i)
    mkdir -p "${MOUNT_BASE}/Disk_${DIR_NAME}"
    
    # Calculate exact byte offset for this specific sector
    OFFSET=$((START_OFFSET + (i * BLOCK_BYTES)))
    
    # Mount the specific chunk (NO FORMATTING!)
    sudo mount -o loop,offset=$OFFSET,sizelimit=1474560,umask=000 $BIN_FILE "${MOUNT_BASE}/Disk_${DIR_NAME}"
done

echo "[+] Connecting Virtual USB to CNC (Read Only)..."
sudo modprobe g_mass_storage file=$BIN_FILE stall=0 ro=1 removable=1

echo "[SUCCESS] Emulation running. Folders mounted at $MOUNT_BASE"
while true; do sleep 1; done