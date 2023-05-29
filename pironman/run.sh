#!/usr/bin/with-contenv bashio
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

sudo /usr/local/bin/pironman start -f \
    -u $temperature_unit \
    -f $fan_temp \
    -al $display_always_on \
    -s $display_on_for \
    -rw $rgb_on \
    -rs $rgb_style \
    -rc $rgb_color \
    -rb $rgb_speed \
    -pwm $rgb_freq \
    -rp $rgb_pin
