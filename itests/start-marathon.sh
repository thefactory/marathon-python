#!/bin/bash

if [[ $MARATHONVERSION != '0.8.1' ]]; then
  LOGGER="--no-logger"
else
  LOGGER=""
fi

java -version
export MESOS_WORK_DIR='/tmp/mesos'
mkdir -p "$MESOS_WORK_DIR"
exec /usr/bin/marathon --master local $LOGGER --hostname localhost
