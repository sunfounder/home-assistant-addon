#!/usr/bin/with-contenv /usr/bin/bashio

rgb_led_count=$(bashio::config "rgb_led_count")
# start pironman5 service
/opt/pironman5/venv/bin/pironman5 --config-path /data/config.json -rl $rgb_led_count start

# test loop
# while true; do
#     echo "test loop"
#     sleep 10
# done
