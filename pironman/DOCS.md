# Pironman Tutorial

> This addon only works with **Home Assistant OS running on a Raspberry Pi**.
> It does not work with Home Assistant Container or other installation methods.

The addon shows hardware information (CPU temperature, usage, RAM, disk, IP
address) on the Pironman OLED display, controls the fan and the RGB strip,
and shuts down the Home Assistant host when the power button is long-pressed.

## Install

1. In Home Assistant, go to **Settings -> Apps -> App store -> Repositories** (three-dot menu) and add the SunFounder repository:
   `https://github.com/sunfounder/home-assistant-addon`
2. Refresh the store, find the **Pironman** addon and install it.
3. Open the **Configuration** tab of the addon and set the options, in particular:
   - `rgb_pin`: how the RGB strip of your case is driven.
     - `10` (SPI): newer Pironman cases (default).
     - `12` (PWM): early Pironman cases, the RGB uses the audio channel.
     - `21` (PCM): cases wired for the PCM output.
4. Start the addon.

## First start (boot configuration)

Current Home Assistant OS releases ship with I2C/SPI disabled. On start, the
addon automatically checks and prepares the boot configuration
(`config.txt` + `CONFIG/modules` on the boot partition), enabling:

- I2C (OLED display),
- SPI + fixed core frequency (SPI RGB, when `rgb_pin` is 10), or audio off
  (PWM RGB, when `rgb_pin` is 12),
- the `gpio-poweroff` overlay (complete power-off on shutdown),
- the `gpio-ir` overlay (IR remote receiver).

**Reboot Home Assistant once** after the first start of the addon (the addon
logs a warning when a reboot is required). The fan and the power button work
immediately; the OLED display and the RGB strip start working after the reboot.

## Manual boot configuration (fallback)

If the addon cannot prepare the boot configuration for you, configure it
manually. You will need:

 - SD card reader
 - SD card with Home Assistant Operating System flashed on it

Shutdown/turn-off your Home Assistant installation and unplug the SD card. Plug the SD card into an SD card reader and find a drive/file system named `hassos-boot`. The file system might be shown/mounted automatically. If not, use your operating systems disk management utility to find the SD card reader and make sure the first partition is available.

- In the root of the `hassos-boot` partition, **add a new folder called** `CONFIG`.
- In the `CONFIG` folder, **add another new folder called** `modules`.
- Inside the `modules` folder, **add a text file called** `rpi-i2c.conf` with the following content:
  ```
  i2c-dev
  ```
- In the root of the `hassos-boot` partition, **edit the file called** `config.txt` **add four lines** to it:
  ```
  dtparam=i2c_vc=on
  dtparam=i2c_arm=on
  dtoverlay=gpio-poweroff,gpio_pin=26,active_low=0
  dtoverlay=gpio-ir,gpio_pin=13
  ```
- To enable RGB, selected one driver and make sure you set up the main board respectivly. continue editing the `config.txt` file:
  > Earlier version of pironman only have one driver, PWM(GPIO12).
  - For PWM(GPIO12), it use audio to drive the led, so turn off the audio.
    ```
    dtparam=audio=off
    ```
  - For SPI(GPIO10), it use spi to drive the led, so turn on the spi, set core freq to 500. Enable audio if you need it.
    ```
    dtparam=spi=on
    core_freq=500
    core_freq_min=500
    # Enable audio if you need it.
    dtparam=audio=on
    ```
  - For PCM(GPIO21), it use PCM to drive the led, it doesn't need to set anything. But it will interfer with I2S device, so make sure you disable them, like hifiberry-dac or i2s-mmap. Enable audio if you need it.
    ```
    # Enable audio if you need it.
    dtparam=audio=on
    # Comment out the i2s device.
    # dtoverlay=hifiberry-dac
    # dtoverlay=i2s-mmap
    ```
- Eject the SD card and plug it back into your Raspberry Pi and boot it up.
