ARG BUILD_FROM
FROM $BUILD_FROM

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install python3 git -y

# clone spc
RUN git clone --depth 1 https://github.com/sunfounder/spc.git

# install scp
RUN cd /spc && python3 install.py --disable-autostart --skip-config-txt --skip-reboot

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
