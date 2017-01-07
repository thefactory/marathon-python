FROM ubuntu:14.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
	software-properties-common
RUN add-apt-repository ppa:webupd8team/java
RUN echo "debconf shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
RUN echo "debconf shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y -q install \
	lsb-release \
	oracle-java8-installer

# Setup
ADD ./marathon-version /root/marathon-version
ADD ./install-marathon.sh /root/install-marathon.sh
RUN /root/install-marathon.sh

EXPOSE 8080
ADD ./start-marathon.sh /root/start-marathon.sh
CMD /etc/init.d/zookeeper start && /root/start-marathon.sh
