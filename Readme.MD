# SunFounder Addon for Home assistant


## Login the running addon container for debgging

Find the container name
```
docker ps
```

replace the `<container_name>` in the following command
```
docker exec -it <container_name> /bin/bash
```

## Home Assistant Supervisor log

See supervisor log for appon reflash and install errors

```
docker logs hassio_supervisor -f
```

## Pironman Addon

> Currently Pironman Addon is in Beta with following knowing issue:
>   1. RGB not working.
>   2. Long press power button to soft power off the pi is not working

### Tutorial

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
