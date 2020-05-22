#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Default version of marathon to test against if not set by the user
[[ -f /root/marathon-version ]] && source /root/marathon-version
MARATHONVERSION="${MARATHONVERSION:-v1.6.322}"

export DEBIAN_FRONTEND=noninteractive

shopt -s extglob

case "${MARATHONVERSION}" in
  v1.9.109)
    echo "Marathon version ${MARATHONVERSION} needs no specific changes"
    apt update
    ;;
  v1.6.322)
    sed -i 's!deb http://ftp.debian.org/debian jessie-backports main!!g' /etc/apt/sources.list
    apt update
    apt install -y mesos=1.6.*
    ;;
  v1.4.11)
    sed -i 's!deb http://ftp.debian.org/debian jessie-backports main!!g' /etc/apt/sources.list
    apt update
    ;;
  @(v1.3.0|v1.1.2))
    rm /etc/apt/sources.list.d/jessie-backports.list
    apt update
    ;;
  *)
    echo "Marathon version ${MARATHONVERSION} is not supported"
    exit 1
    ;;
esac

apt install -y --force-yes zookeeperd curl lsof
rm -rf /var/log/apt/* /var/log/alternatives.log /var/log/bootstrap.log /var/log/dpkg.log
