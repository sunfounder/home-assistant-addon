ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools procps -y

# clone pironman
RUN git clone -b test --depth 1 https://github.com/sunfounder/pironman.git

# install pironman
RUN cd /pironman && python3 install.py --skip-config-txt --skip-auto-startup --skip-reboot

# set the working directory to /data/pironman
WORKDIR /data

# copy run.sh
COPY run.sh /
# add execute permission
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]


# COPY test.sh /
# RUN chmod a+x /test.sh
# CMD [ "/test.sh" ]
