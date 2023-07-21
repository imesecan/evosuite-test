#!/bin/bash
#
# Usage:
#   ./generate-tests.sh  CONTAINER RUNTIME  JOBID  PREFIX TARGET_CLASS TARGET_FUNCTION 
#
# Sample usage:
#   Ex1:  ./generate-tests.sh  Classify 60   112  "org leakreducer"  Classify  classify
#	Ex2:  ./generate-tests.sh  01-Aliasing-ControlFlow-insecure  60  128  "org leakreducer"  Main  process   
#	Ex1:  Run Sanitizers for 60 seconds using 112 as the randomization seed 
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
TARGET_FUNCTION=$6

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

python3 retrieve-functional-tests.py --trg_prj ${CONTAINER}  --trg_cls ${TRG_CLS} \
			--trg_function ${TARGET_FUNCTION}  --jobid ${JOBID}  \
			> evosuite-tests/${TRG_CLS}-${JOBID}-driver-input.txt
date
