#!/bin/bash
set -vxeu

# Default version of marathon to test against if not set by the user
[[ -f /root/marathon-version ]] && source /root/marathon-version
MARATHONVERSION="${MARATHONVERSION:-0.8.2}"

sudo apt-get update -q

# Setup
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
CODENAME=$(lsb_release -cs)

# Add the repository
echo "deb http://repos.mesosphere.com/${DISTRO} ${CODENAME} main" | 
  sudo tee /etc/apt/sources.list.d/mesosphere.list
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get -y update

# Install packages
sudo apt-get -y --force-yes install mesos marathon=$MARATHONVERSION*
