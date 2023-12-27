#!/usr/bin/with-contenv /usr/bin/bashio
CONFIG_PATH=/data/options.json

mqtt_host=$(bashio::config 'mqtt_host')
mqtt_port=$(bashio::config 'mqtt_port')
mqtt_username=$(bashio::config 'mqtt_username')
mqtt_password=$(bashio::config 'mqtt_password')
ssl=$(bashio::config 'ssl')
ssl_cafile=$(bashio::config 'ssl_cafile')
ssl_certfile=$(bashio::config 'ssl_certfile')

echo "Starting spc with the following parameters:"
echo "MQTT host: $mqtt_host"
echo "MQTT port: $mqtt_port"
echo "MQTT username: $mqtt_username"
echo "MQTT password: $mqtt_password"
echo "SSL: $ssl"
echo "SSL CA file: $ssl_cafile"
echo "SSL cert file: $ssl_certfile"

if [[ $ssl ]]; then
    ssl_config="--ssl --ssl-cafile $ssl_cafile --ssl-certfile $ssl_certfile"
else
    ssl_config=""
fi

python3 /opt/spc/spc_server start --mqtt-host $mqtt_host --mqtt-port $mqtt_port --mqtt-username $mqtt_username --mqtt-password $mqtt_password $ssl_config
