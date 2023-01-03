#!/bin/bash
# This script is not for direct usage. It is called by another script
# Usage:
#    ./run.sh  TEST_SUBJECT  JOBID
# Sample usage:
#    ./run.sh  Sanitizers  135 
#

SRC=$1
JOBID=$2

cd ${SRC}
./genFunctionalTests.sh ${JOBID}
mv ${SRC}-${JOBID}  ../
