ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools procps -y

# add github branch ref to invalidating the docker cache.
ADD https://api.github.com/repos/sunfounder/pironman/git/refs/heads/v2.0 version.json
# clone pironman
RUN git clone -b v2.0 --depth 1 https://github.com/sunfounder/pironman.git

# pironman v2.0 install.py installs libtiff5-dev, which does not exist on
# Ubuntu 24.04 (noble) used by ubuntu-base 10.x; libtiff-dev is the replacement.
RUN sed -i 's/libtiff5-dev/libtiff-dev/g' /pironman/install.py

# install pironman
RUN cd /pironman && python3 install.py --skip-config-txt --skip-auto-startup --skip-reboot

# set the working directory to /data/pironman
WORKDIR /data

# copy run.sh
COPY run.sh /
# add execute permission
RUN chmod a+x /run.sh

# copy boot config helper (enables I2C/SPI and overlays on Home Assistant OS)
COPY boot-config.sh /
RUN chmod a+x /boot-config.sh

CMD [ "/run.sh" ]
