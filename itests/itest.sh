#!/bin/bash

set -e

[[ -n $TRAVIS ]] || echo MARATHONVERSION=$MARATHONVERSION > marathon-version
[[ -n $TRAVIS ]] || docker-compose build
[[ -n $TRAVIS ]] || docker-compose pull
[[ -n $TRAVIS ]] || docker-compose up -d
behave "$@"
[[ -n $TRAVIS ]] || docker-compose stop
[[ -n $TRAVIS ]] || docker-compose rm --force
