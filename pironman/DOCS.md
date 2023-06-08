# Pironman Tutorial

## Setup config.txt

You need to setup config.txt to enable I2C and SPI.

> This only works for Home Assistant OS, running on Raspberry Pi. Not for Home Assistant Container. Which means this only support for the os install on Raspbberry Pi. Not for the docker container.

You will need:

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
 - To enable RGB, selected one driver and make sure you set up the main board respectivly. Add more lines to the `config.txt` file:
   - For SPI(GPIO10)
      ```
      dtparam=spi=on
      dtparam=audio=on
      core_freq=500
      core_freq_min=500
      ```
   - For PCM(GPIO21)
      ```
      dtparam=audio=on
      dtoverlay=hifiberry-dac
      ```
   - For PWM(GPIO12)
      ```
      dtparam=audio=off
      ```
 - Eject the SD card and plug it back into your Raspberry Pi and boot it up.
