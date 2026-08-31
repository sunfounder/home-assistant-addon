# Pironman Addon

This is an addon for [SunFounder Pironman](https://www.sunfounder.com/products/raspberry-pi-4-case?_pos=1&_sid=fbd7f34c4&_ss=r). Allow you to checkout hardware informations on the OLED, control fan, and RGB lights.

![pironman](https://raw.githubusercontent.com/sunfounder/home-assistant-addon/main/pironman/img/pironman.webp)

## Home Assistant OS compatibility

- Works on current Home Assistant OS releases (tested on HA OS 18 with
  Home Assistant 2026.8).
- On first start the addon automatically prepares the boot configuration
  (I2C, SPI, power/IR overlays). Reboot Home Assistant once after the first
  start; the OLED display and RGB strip become available after the reboot.

See [DOCS.md](DOCS.md) for the full setup instructions.
