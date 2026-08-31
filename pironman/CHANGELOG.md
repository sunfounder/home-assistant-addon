# Changelog

## [1.0.13] - 2026-8-31

### Added
- Automatically prepare the Home Assistant OS boot configuration (I2C, SPI and power/IR overlays) on first start, so the OLED display and RGB strip work on current Home Assistant OS releases without editing the SD card by hand.

### Fixed
- Rebuild support: switched the base image from Ubuntu 20.04 (end of life, apt repositories no longer available) to Ubuntu 24.04 and patched the pironman installer for the new base (`libtiff5-dev` -> `libtiff-dev`).
- Fixed the aarch64 build to use the 64-bit base image instead of the 32-bit armv7 one.

## [1.0.12] - 2024-5-23

### Fixed
- Fixed rebuild on boot 5
