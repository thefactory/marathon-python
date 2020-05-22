ARG MARATHONVERSION=v1.6.322
FROM mesosphere/marathon:$MARATHONVERSION
USER root

# Setup
ADD ./marathon-version /root/marathon-version
ADD ./install-marathon.sh /root/install-marathon.sh
RUN /root/install-marathon.sh

EXPOSE 8080 5050
ADD ./start-marathon.sh /root/start-marathon.sh
ENTRYPOINT []
CMD ["/root/start-marathon.sh"]
