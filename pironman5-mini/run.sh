#!/usr/bin/with-contenv /usr/bin/bashio

# start pironman5 service
/opt/pironman5/venv/bin/pironman5-service --config-path /data/config.json start

# test loop
# while true; do
#     echo "test loop"
#     sleep 10
# done
