ARG MARATHONVERSION=v1.6.322
FROM mesosphere/marathon:$MARATHONVERSION
ARG MARATHONVERSION
USER root

# Setup
ADD ./install-marathon.sh /root/install-marathon.sh
RUN echo "MARATHONVERSION=${MARATHONVERSION}" > /root/marathon-version \
  && /root/install-marathon.sh

EXPOSE 8080 5050
ADD ./start-marathon.sh /root/start-marathon.sh
ENTRYPOINT []
CMD ["/root/start-marathon.sh"]
