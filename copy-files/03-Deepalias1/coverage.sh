#!/bin/bash
#
# Using maven, jacoco and current test inputs from driver-input.txt,
#    prepare unit test and then coverage file.
#
# Sample usage 
#    ./coverage.sh 
# The result file stored in
#    "project_root_folder/target/site/jacoco/jacoco.xml"
#

make clean
set -a
. constants.sh
set +a
cd $SRC
VAR=$(javac ${DRIVER}${EXT} 2>&1)

if echo "$VAR" | grep -qi "error:"; then
  echo "error: $VAR"
else
	python3 driver.py
	python3 coverage.py
	cd -
	mvn clean install
fi
