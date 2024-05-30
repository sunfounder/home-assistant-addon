ARG BUILD_FROM
FROM $BUILD_FROM

# Create directory /tmp/boot
RUN mkdir -p /tmp/boot

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install requests

WORKDIR /data

COPY pi-config-wizard /pi-config-wizard

COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
