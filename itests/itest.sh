#!/bin/bash

set -e

[[ -n $TRAVIS ]] || docker pull "missingcharacter/marathon-python:${MARATHONVERSION}"
[[ -n $TRAVIS ]] || docker run --rm --name marathon-python -d -p 18080:8080 -p 15050:5050 "missingcharacter/marathon-python:${MARATHONVERSION}"
behave "$@"
[[ -n $TRAVIS ]] || docker kill marathon-python
