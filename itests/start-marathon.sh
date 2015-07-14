#!/bin/bash

if [[ $MARATHONVERSION != '0.8.1' ]]; then
  LOGGER="--no-logger"
else
  LOGGER=""
fi

exec marathon --master local $LOGGER --hostname localhost
