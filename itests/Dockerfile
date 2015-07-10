FROM ubuntu-debootstrap:14.04
RUN apt-get update && apt-get -y install sudo lsb-release

# Setup
ADD ./install-marathon.sh /root/install-marathon.sh
RUN /root/install-marathon.sh

EXPOSE 8080
CMD /etc/init.d/zookeeper start && marathon --master local --no-logger
