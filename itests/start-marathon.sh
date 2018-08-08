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
nohup  mesos-master --work_dir=/tmp/mesosmaster --zk=$ZK_HOST --quorum=1 &
nohup mesos-agent --master=$ZK_HOST --work_dir=/tmp/mesosagent --launcher=posix &
exec /usr/bin/marathon --master $ZK_HOST $LOGGER 
