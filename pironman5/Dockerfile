ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools -y

# Install libraspberrypi-bin for vcgencmd
RUN apt-get install -y libraspberrypi-bin

# clone pironman 5
RUN git clone https://github.com/sunfounder/pironman5.git -b 1.2.6

# install pironman
RUN cd /pironman5 && python3 install.py --skip-auto-start --skip-reboot --skip-dtoverlay --skip-modules --plain-text

# uninstall rpi.gpio
RUN /opt/pironman5/venv/bin/pip uninstall RPi.GPIO -y
# install rpi.lgpio instead
RUN /opt/pironman5/venv/bin/pip install rpi.lgpio
RUN pip install rpi.lgpio --break

# downgrade adafruit-blinka to 8.55.0
RUN /opt/pironman5/venv/bin/pip install adafruit-blinka==8.55.0

# set the working directory to /data/pironman
WORKDIR /data

# copy run.sh
COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
