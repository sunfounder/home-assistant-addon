# SunFounder Addon for Home assistant

- [SunFounder Addon for Home assistant](#sunfounder-addon-for-home-assistant)
  - [Pironman Addon](#pironman-addon)
    - [Tutorial](#tutorial)
      - [Setup config.txt](#setup-configtxt)
      - [Install the Addon](#install-the-addon)
        - [Click the button below to install the addon](#click-the-button-below-to-install-the-addon)
        - [Or install it manually:](#or-install-it-manually)
      - [Setup](#setup)
      - [Configure](#configure)
  - [Development](#development)
    - [Cleanup image cache](#cleanup-image-cache)
    - [Login the running addon container for debgging](#login-the-running-addon-container-for-debgging)
    - [Home Assistant Supervisor log](#home-assistant-supervisor-log)
    - [App Armor](#app-armor)
  - [Publish](#publish)


## Pironman Addon

### Tutorial

#### Setup config.txt

You need to setup config.txt to enable I2C and SPI for Pironman.

> This only works for Home Assistant OS, running on Raspberry Pi. Not for Home Assistant Container.

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
- In the root of the `hassos-boot` partition, **edit the file called** `config.txt` **add four lines** to the bottom:
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

#### Install the Addon

##### Click the button below to install the addon

[![Open your Home Assistant instance and show the dashboard of a Supervisor add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=6fa7f6d2_pironman&repository_url=https%3A%2F%2Fgithub.com%2Fsunfounder%2Fhome-assistant-addon)

##### Or install it manually:

1. On Home Assistant, navigator to Configuration -> Addons -> Addon Store
2. Click the top right corner button to open the menu, select Repositories
3. Type in the repository url: `https://github.com/sunfounder/home-assistant-addon`, click Add
4. After **SunFounder** repository added, close the popup window
5. Click the top right corner button again to open the menu, select **Reload**
6. Wait a few seconds, the **SunFounder** repository will show up in the addon store with Pironman following. If not, try to refresh the page.
7. Click on Pironman, then click Install.

#### Setup

Currently, you need to disable protection mode to allow the addon to access hardware informations.

To do so, in Pironman addon page, (Configuration -> Addons -> Pironman). Find Protection Mode, and turn it off. Then, restart the addon.

Change to the Log tab, and see if there's any error. If not, you can continue to the next step.

#### Configure

You can change the configuration in the Configuration tab. Navigate to Configuration tab, and change the settings.



## Development

Development instruction for addon developer.

### Cleanup image cache

Image may not be updated after rebuild. To force rebuild, you need to clean up the image cache.
uninstall the addon first, then run the following command to clean up the image cache.

```
docker image prune -af
```

### Login the running addon container for debgging

Find the container name
```
docker ps
```

replace the `<container_name>` in the following command
```
docker exec -it <container_name> /bin/bash
```

### Home Assistant Supervisor log

See supervisor log for appon reflash and install errors

```
docker logs hassio_supervisor -f
```

### App Armor

Check if complain enabled

```
docker inspect addon_local_pironman | grep "AppArmorProfile"
```

## Publish

进入需要编译的插件根目录下，执行以下命令：
注意修改名称和版本号。注意确认基础镜像的版本号。
可以在Windows下执行，但是需要安装Docker Desktop, 然后运行。
需要编译4个版本，aarch64和armv7，每个版本有两个tag，一个是版本号，一个是latest。

```bash
docker build . --build-arg BUILD_FROM=ghcr.io/hassio-addons/ubuntu-base/aarch64:10.0.1 -t sunfounder/aarch64-pironman5:1.0.2
docker build . --build-arg BUILD_FROM=ghcr.io/hassio-addons/ubuntu-base/aarch64:10.0.1 -t sunfounder/aarch64-pironman5-mini:1.0.1
```

给版本打上latest标签。

```bash
docker tag sunfounder/aarch64-pironman5:1.0.2 sunfounder/aarch64-pironman5:latest
docker tag sunfounder/aarch64-pironman5-mini:1.0.1 sunfounder/aarch64-pironman5-mini:latest
```

登录docker。如果在Windows下，登录了Docker Desktop，可以省略这一步。

```bash
docker login
```

上传4个镜像。注意修改版本号。

```bash
docker push sunfounder/aarch64-pironman5:1.0.2
docker push sunfounder/aarch64-pironman5:latest
```
