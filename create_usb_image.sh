#!/bin/bash
set -euo pipefail

OUT="/home/pizerocnc2/original_cnc_image.bin"
NUM_DISKS=101
BLOCK_BYTES=1572864
FLOPPY_BYTES=1474560

echo "[+] Creating empty container: $OUT"
truncate -s $(( (NUM_DISKS + 1) * BLOCK_BYTES )) "$OUT"

for i in $(seq 0 $NUM_DISKS); do
    OFFSET=$(( i * BLOCK_BYTES ))
    LABEL=$(printf "DISK%03d" "$i")
    TMP_LOOP=""

    echo "[+] Formatting slot $i at offset $OFFSET with label $LABEL"

    TMP_LOOP=$(sudo losetup -f --show -o "$OFFSET" --sizelimit "$FLOPPY_BYTES" "$OUT")
    sudo mkfs.fat -F 12 -n "$LABEL" "$TMP_LOOP" >/dev/null
    sudo losetup -d "$TMP_LOOP"
done

echo "[+] Demo image created: $OUT"
ls -lh "$OUT"
