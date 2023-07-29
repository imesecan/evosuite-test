#!/bin/bash
#
# Sample usage 
#    ./build.sh 
#

make clean
set -a
. constants.sh
set +a
cd $SRC
VAR=$(javac ${DRIVER}${EXT} 2>&1)

if echo "$VAR" | grep -q "error:"; then
  echo "error: $VAR"
else
	python3 driver.py
fi
