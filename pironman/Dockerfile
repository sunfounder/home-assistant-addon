FROM ghcr.io/hassio-addons/ubuntu-base/aarch64:8.2.1

# update apt-get
RUN apt-get update

# install dependencies
RUN apt-get install git python3 python3-pip python3-setuptools sudo -y

# mount config.txt to /boot/firmware
RUN if [ -e /dev/sda1 ]; then \
  mkdir /boot; \
  mkdir /boot/firmware; \
  mount /dev/sda1 /boot/firmware; \
  ls /boot/firmware; \
else \
  echo "No /dev/sda1"; \
fi

# set the working directory to /data/pironman
WORKDIR /data

# clone pironman
RUN cd /data && git clone -b v2.0 --depth 1 https://github.com/sunfounder/pironman.git

# install pironman
RUN cd /data/pironman && python3 install.py --skip-config-txt --skip-auto-startup --skip-reboot

# copy run.sh
COPY run.sh /data

# add execute permission
RUN chmod a+x /data/run.sh

CMD [ "ls /data ;; ls / ;; echo $HASSIO_HOST ;;/data/run.sh" ]
