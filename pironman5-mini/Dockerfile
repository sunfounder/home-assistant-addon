ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools -y

# clone pironman 5
ADD https://api.github.com/repos/sunfounder/pironman5-mini/git/refs/heads/main version.json
RUN git clone https://github.com/sunfounder/pironman5-mini.git

# install pironman
RUN cd /pironman5-mini && python3 install.py --skip-auto-start --skip-reboot --skip-dtoverlay --plain-text

# set the working directory to /data/pironman
WORKDIR /data

# copy run.sh
COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
