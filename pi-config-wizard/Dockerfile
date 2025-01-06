ARG BUILD_FROM
FROM $BUILD_FROM

# Create directory /tmp/boot
RUN mkdir -p /tmp/boot

# Update APT
RUN apt-get update

# Install Python3 and pip
RUN apt-get install -y python3 python3-pip

# Install requests module
RUN pip3 install requests --break

# Copy pi-config-wizard to /data
WORKDIR /data

# Copy pi-config-wizard to /data
COPY pi-config-wizard /pi-config-wizard

# Copy run.sh to /
COPY run.sh /

# Set permissions for run.sh
RUN chmod a+x /run.sh

# Set default command
CMD [ "/run.sh" ]
