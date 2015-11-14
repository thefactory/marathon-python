#!/bin/bash

if [[ $MARATHONVERSION != '0.8.1' ]]; then
  LOGGER="--no-logger"
else
  LOGGER=""
fi

java -version
exec /usr/bin/marathon --master local $LOGGER --hostname localhost
