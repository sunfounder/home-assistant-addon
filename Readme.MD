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