#!/usr/bin/env bash
set -xeuo pipefail
IFS=$'\n\t'

LOGGER="--logging_level info"
# Default version of marathon to test against if not set by the user
[[ -f /root/marathon-version ]] && source /root/marathon-version
MARATHONVERSION="${MARATHONVERSION:-v1.6.322}"

shopt -s extglob

case "${MARATHONVERSION}" in
  @(v1.4.11|v1.3.0|v1.1.2))
    ln -sf /marathon/bin/start /marathon/bin/marathon
    ;;
  *)
    echo "Marathon version ${MARATHONVERSION} needs no specific changes"
    ;;
esac

java -version
export MESOS_WORK_DIR='/tmp/mesos'
export ZK_HOST=$(cat /etc/mesos/zk)

mkdir -p "${MESOS_WORK_DIR}"
/etc/init.d/zookeeper start
nohup mesos-master --work_dir=/tmp/mesosmaster --zk=${ZK_HOST} --quorum=1 &> mesos-master.log &
nohup /usr/bin/env MESOS_SYSTEMD_ENABLE_SUPPORT=false mesos-slave --master=${ZK_HOST} --work_dir=/tmp/mesosagent --launcher=posix &> mesos-agent.log &
eval "bin/marathon --master ${ZK_HOST} ${LOGGER}"
