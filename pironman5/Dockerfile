ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools -y

# clone pironman 5
ADD https://api.github.com/repos/sunfounder/pironman5/git/refs/heads/main version.json
RUN git clone https://github.com/sunfounder/pironman5.git

# install pironman
RUN cd /pironman5 && python3 install.py --skip-auto-start --skip-reboot --skip-dtoverlay --skip-modules --plain-text

# Replace old version of these packages for compatibility
RUN /opt/pironman5/venv/bin/pip3 install adafruit_blinka==8.39.2 gpiod==1.5.4

# set the working directory to /data/pironman
WORKDIR /data

# copy run.sh
COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
