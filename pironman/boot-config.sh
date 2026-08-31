#!/bin/bash
# Pironman boot configuration for Home Assistant OS.
#
# Modern Home Assistant OS releases ship with I2C/SPI disabled. The Pironman
# case needs them (plus the power/IR overlays) for the OLED display, the RGB
# strip and the power button to work. This script mounts the boot partition,
# updates config.txt and CONFIG/modules and reports whether a reboot is
# required. It is idempotent and safe to run on every start.
#
# Usage: boot-config.sh <rgb_pin>    # rgb_pin: 10 (SPI) | 12 (PWM) | 21 (PCM)
#
# Exit codes:
#   0 - boot config is up to date, nothing to do
#   1 - boot config was updated or is applied but a host reboot is still pending
#   2 - failed to check/update the boot config

RGB_PIN="${1:-10}"
BOOT_MOUNT="/tmp/boot"
CONFIG_TXT="$BOOT_MOUNT/config.txt"
MODULES_CONF="$BOOT_MOUNT/CONFIG/modules/rpi-i2c.conf"

log() { echo "[boot-config] $*" >&2; }

# Replace the first line starting with search_key by newline, or append it.
edit_config_txt() {
    local search_key="$1" newline="$2" line found=0
    local tmp
    tmp="$(mktemp)"
    while IFS= read -r line; do
        if [ "$found" = 0 ] && [[ "$line" == "$search_key"* ]]; then
            printf '%s\n' "$newline" >> "$tmp"
            found=1
        else
            printf '%s\n' "$line" >> "$tmp"
        fi
    done < "$CONFIG_TXT"
    if [ "$found" = 0 ]; then
        printf '%s\n' "$newline" >> "$tmp"
    fi
    mv "$tmp" "$CONFIG_TXT"
}

has_config() { grep -qxF "$1" "$CONFIG_TXT" 2>/dev/null; }

# Extract the config.txt option name used for matching:
#   "dtoverlay=gpio-ir,gpio_pin=13" -> "dtoverlay=gpio-ir"  (key ends at first comma)
#   "dtparam=i2c_arm=on"           -> "dtparam=i2c_arm"    (key ends before the value)
config_key() {
    local line="$1" key
    if echo "$line" | grep -q ','; then
        key="$(echo "$line" | cut -d, -f1)"
    else
        key="$(echo "$line" | sed 's/=[^=]*$//')"
    fi
    printf '%s\n' "$key"
}

# ---- required config.txt lines depending on the RGB pin -----------------
REQUIRED_LINES="dtparam=i2c_arm=on
dtparam=i2c_vc=on
dtoverlay=gpio-poweroff,gpio_pin=26,active_low=0
dtoverlay=gpio-ir,gpio_pin=13"
case "$RGB_PIN" in
    10)  # SPI driven RGB: enable SPI and fix the core frequency
        REQUIRED_LINES="$REQUIRED_LINES
dtparam=spi=on
core_freq=500
core_freq_min=500"
        ;;
    12)  # PWM driven RGB: uses the audio channel, audio must be off
        REQUIRED_LINES="$REQUIRED_LINES
dtparam=audio=off"
        ;;
    21)  # PCM driven RGB: nothing extra needed
        ;;
    *)
        log "unknown rgb_pin '$RGB_PIN', treating as SPI (10)"
        REQUIRED_LINES="$REQUIRED_LINES
dtparam=spi=on
core_freq=500
core_freq_min=500"
        ;;
esac

# ---- locate the boot partition (same approach as pi-config-wizard) ------
DATA_PART="$(df /data 2>/dev/null | awk 'NR==2 {print $1}')"
if [ -z "$DATA_PART" ]; then
    log "cannot locate the /data partition"
    exit 2
fi
DISK="$(lsblk -no pkname "$DATA_PART" 2>/dev/null)"
if [ -z "$DISK" ]; then
    log "cannot locate the parent disk of $DATA_PART"
    exit 2
fi
BOOT_PART="/dev/$(lsblk -no kname "/dev/$DISK" 2>/dev/null | grep -v "^$DISK$" | sort -V | head -n1)"
if [ -z "$BOOT_PART" ] || [ ! -e "$BOOT_PART" ]; then
    log "cannot locate the boot partition on $DISK"
    exit 2
fi

# ---- mount boot partition ----------------------------------------------
mkdir -p "$BOOT_MOUNT"
if ! mountpoint -q "$BOOT_MOUNT"; then
    if ! mount -t vfat "$BOOT_PART" "$BOOT_MOUNT" >/dev/null 2>&1; then
        log "failed to mount $BOOT_PART"
        exit 2
    fi
fi
if [ ! -f "$CONFIG_TXT" ]; then
    log "config.txt not found on $BOOT_PART"
    umount "$BOOT_MOUNT" 2>/dev/null
    exit 2
fi

# ---- check current state (after mounting) -------------------------------
I2C_OK=0
[ -e /dev/i2c-1 ] && I2C_OK=1
SPI_OK=0
[ -e /dev/spidev0.0 ] && SPI_OK=1

NEED_WRITE=0
NEED_REBOOT=0

# devices that are required but not present yet?
[ "$I2C_OK" = 0 ] && NEED_REBOOT=1
if [ "$RGB_PIN" = 10 ] && [ "$SPI_OK" = 0 ]; then
    NEED_REBOOT=1
fi

# required config lines / modules file present?
# Right after a host reboot the boot partition can be briefly rewritten by
# the host itself, so retry the modules file check before concluding it is
# missing.
MODULES_OK=0
for _attempt in 1 2 3; do
    if [ -f "$MODULES_CONF" ] && grep -qxF 'i2c-dev' "$MODULES_CONF" 2>/dev/null; then
        MODULES_OK=1
        break
    fi
    sleep 2
done
[ "$MODULES_OK" = 0 ] && NEED_WRITE=1
while IFS= read -r line; do
    has_config "$line" || { NEED_WRITE=1; break; }
done <<< "$REQUIRED_LINES"

# ---- update what is missing ---------------------------------------------
if [ "$NEED_WRITE" = 1 ]; then
    mkdir -p "$BOOT_MOUNT/CONFIG/modules"
    grep -qxF 'i2c-dev' "$MODULES_CONF" 2>/dev/null || echo 'i2c-dev' >> "$MODULES_CONF"
    while IFS= read -r line; do
        has_config "$line" || edit_config_txt "$(config_key "$line")" "$line"
    done <<< "$REQUIRED_LINES"
    sync
    log "boot config updated on $BOOT_PART:"
    log "$REQUIRED_LINES"
else
    log "boot config already applied"
fi

umount "$BOOT_MOUNT" 2>/dev/null

if [ "$NEED_REBOOT" = 1 ]; then
    log "a host reboot is required (i2c-1: $I2C_OK, spidev0.0: $SPI_OK)"
    exit 1
fi
log "boot config OK (i2c-1: $I2C_OK, spidev0.0: $SPI_OK)"
exit 0
