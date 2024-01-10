#!/usr/bin/with-contenv /usr/bin/bashio
CONFIG_PATH=/data/options.json

unit=$(bashio::config 'unit')
rgb_enable=$(bashio::config 'rgb_enable')
rgb_style=$(bashio::config 'rgb_style')
rgb_color=$(bashio::config 'rgb_color')
rgb_speed=$(bashio::config 'rgb_speed')
rgb_num=$(bashio::config 'rgb_num')
rgb_freq=$(bashio::config 'rgb_freq')
rgb_pin=$(bashio::config 'rgb_pin')

echo "Starting pironman with the following parameters:"
echo "unit: $unit"
echo "rgb_enable: $rgb_enable"
echo "rgb_style: $rgb_style"
echo "rgb_color: $rgb_color"
echo "rgb_speed: $rgb_speed"
echo "rgb_num: $rgb_num"
echo "rgb_freq: $rgb_freq"
echo "rgb_pin: $rgb_pin"

bash /usr/local/bin/pironman5 start -F \
    -u $unit \
    -re $rgb_enable \
    -rs $rgb_style \
    -rc $rgb_color \
    -rb $rgb_speed \
    -rn $rgb_num \
    -fq $rgb_freq \
    -rp $rgb_pin
