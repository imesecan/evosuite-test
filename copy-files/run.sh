#!/bin/bash
# This script is not for direct usage. It is called by another script
# Usage:
#    ./run.sh   SRC  RUNTIME   JOBID  TRG_CLS
# Sample usage:
#    ./run.sh  Sanitizers  60 135 Sanitizers1
#

SRC=$1					# Foldername
RUNTIME=$2				# runtime in seconds
JOBID=$3				# unique id to describe this job
TRG_CLS=$4				# target class name

cd ${SRC}
./genFunctionalTests.sh  ${RUNTIME}  ${JOBID}  ${TRG_CLS}
mv ${SRC}-${JOBID}  ../
