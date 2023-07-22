#!/bin/bash
# This script is not for direct usage. It is called by another script
# Usage:
#    ./run.sh   SRC  RUNTIME   JOBID  TRG_CLS  PREFIX
# Sample usage:
#    ./run.sh  Classify  60   112  Classify  "org leakreducer"
#

SRC=$1					# Foldername
RUNTIME=$2				# runtime in seconds
JOBID=$3				# unique id to describe this job
TRG_CLS=$4				# target class name
PREFIX=$5				# prefix for package 

echo "Params: ${SRC}  ${RUNTIME}  ${JOBID}  ${PREFIX}  ${TRG_CLS}" > docker-result.txt  2>&1

cd ${SRC}
echo 
./genFunctionalTests.sh  ${RUNTIME}  ${JOBID}  ${TRG_CLS}  "${PREFIX}" \
     	>> docker-result.txt  2>&1

mv docker-result.txt  ${SRC}-${JOBID}/
mv ${SRC}-${JOBID}  ../
