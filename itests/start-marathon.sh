#!/bin/bash

if [[ $MARATHONVERSION != '0.8.1' ]]; then
  LOGGER="--logging_level info"
else
  LOGGER=""
fi

java -version
export MESOS_WORK_DIR='/tmp/mesos'
export ZK_HOST=`cat /etc/mesos/zk`

mkdir -p "$MESOS_WORK_DIR"
exec /usr/bin/marathon --master $ZK_HOST $LOGGER --hostname localhost
