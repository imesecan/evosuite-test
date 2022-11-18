#!/bin/bash
#
# Usage:
#   ./generate-tests.sh  CONTAINER RUNTIME  JOBID  PREFIX TARGET_CLASS
#
# Sample usage:
#   Ex1:  ./generate-tests.sh  Sanitizers  60   112  "securibench micro sanitizers"  Sanitizers1
#   Ex2:  ./generate-tests.sh  01-Deepcall1  360   171 "" program1
#   Ex1:  Run Sanitizers for 60 seconds using 112 as the randomization seed 
#

tolower(){
        echo $(echo $1 | tr '[:upper:]' '[:lower:]');
}

if [[ -z $5 ]]; then
	echo " Error: Missing parameter(s). Usage:"
	echo "  $0   CONTAINER RUNTIME  JOBID  PREFIX  TARGET_CLASS"
	echo " Sample usage:"
	echo "  Ex1: $0  Sanitizers   90   128  \"securibench micro sanitizers\"  Sanitizers1"
	echo "  Ex2: $0  01-Aliasing  90   128 \"\" Main"
	echo ""
  	exit 0
fi

CONTAINER=$1
RUNTIME=$2
JOBID=$3
PREFIX=$4
TRG_CLS=$5

container=$(tolower "$CONTAINER")
container="$container-${JOBID}"
echo "Params: ${CONTAINER} ${RUNTIME} ${JOBID} ${TRG_CLS} - ${container}"

date
mkdir -p evosuite-tests

docker build  -t evosuite  .
docker run --name ${container}  evosuite  /bin/bash  /evosuite/run.sh  \
     ${CONTAINER}  ${RUNTIME}  ${JOBID} "${PREFIX}" ${TRG_CLS}

TRG="${container}:/evosuite/${CONTAINER}-${JOBID}"
docker cp  ${TRG}   "./evosuite-tests/"
docker rm $container
date
