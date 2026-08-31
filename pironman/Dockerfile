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

# On noble, the pip shipped by python3-pip is debian-managed and cannot be
# upgraded in place (no RECORD file), which makes install.py fail the whole
# build. Make the pip upgrade step non-fatal - pip 24.0 is recent enough.
RUN sed -i 's|python3 -m pip install --upgrade pip |python3 -m pip install --upgrade pip \|\| true |' /pironman/install.py

# rpi-ws281x is installed separately from a patched source below.
RUN sed -i "/'rpi-ws281x',/d" /pironman/install.py

# install pironman
RUN cd /pironman && python3 install.py --skip-config-txt --skip-auto-startup --skip-reboot

# rpi-ws281x 5.x on aarch64 reads the board revision from /proc/device-tree,
# which is not exposed inside Home Assistant OS containers. Install a patched
# copy that falls back to /proc/cpuinfo.
COPY rpi-ws281x-cpuinfo-fallback.patch /
RUN apt-get install patch -y && \
    mkdir -p /tmp/ws281x && cd /tmp/ws281x && \
    pip3 download --no-deps --no-binary :all: rpi-ws281x==5.0.0 -d . && \
    tar xzf rpi_ws281x-5.0.0.tar.gz && \
    cd rpi_ws281x-5.0.0 && \
    patch -p1 < /rpi-ws281x-cpuinfo-fallback.patch && \
    pip3 install --break-system-packages --no-deps .

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
