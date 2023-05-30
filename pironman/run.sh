#!/usr/bin/with-contenv bashio
CONFIG_PATH=/data/options.json

temperature_unit=$(bashio::config 'temperature_unit')
fan_temp=$(bashio::config 'fan_temp')
display_always_on=$(bashio::config 'display_always_on')
display_on_for=$(bashio::config 'display_on_for')
rgb_on=$(bashio::config 'rgb_on')
rgb_style=$(bashio::config 'rgb_style')
rgb_color=$(bashio::config 'rgb_color')
rgb_speed=$(bashio::config 'rgb_speed')
rgb_freq=$(bashio::config 'rgb_freq')
rgb_pin=$(bashio::config 'rgb_pin')

CONF="/root/.config/pironman/config.txt"


echo "Starting pironman with the following parameters:"
echo "temperature_unit: $temperature_unit"
echo "fan_temp: $fan_temp"
echo "display_always_on: $display_always_on"
echo "display_on_for: $display_on_for"
echo "rgb_on: $rgb_on"
echo "rgb_style: $rgb_style"
echo "rgb_color: $rgb_color"
echo "rgb_speed: $rgb_speed"
echo "rgb_freq: $rgb_freq"
echo "rgb_pin: $rgb_pin"

ifconfig

sed -i -e "s:temp_unit.*=.*:temp_unit = $temperature_unit:g" ${CONF}
sed -i -e "s:fan_temp.*=.*:fan_temp = $fan_temp:g" ${CONF}
sed -i -e "s:screen_always_on.*=.*:screen_always_on = $display_always_on:g" ${CONF}
sed -i -e "s:screen_off_time.*=.*:screen_off_time = $display_on_for:g" ${CONF}
sed -i -e "s:rgb_switch.*=.*:rgb_switch = $rgb_on:g" ${CONF}
sed -i -e "s:rgb_style.*=.*:rgb_style = $rgb_style:g" ${CONF}
sed -i -e "s:rgb_color.*=.*:rgb_color = $rgb_color:g" ${CONF}
sed -i -e "s:rgb_blink_speed.*=.*:rgb_blink_speed = $rgb_speed:g" ${CONF}
sed -i -e "s:rgb_pwm_freq.*=.*:rgb_pwm_freq = $rgb_freq:g" ${CONF}
sed -i -e "s:rgb_pin.*=.*:rgb_pin = $rgb_pin:g" ${CONF}
sudo /usr/local/bin/pironman start_foreground


