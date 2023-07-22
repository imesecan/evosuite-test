#!/bin/bash
#
# Usage:
#   ./generate-tests.sh  CONTAINER  RUNTIME  JOBID  TARGET_CLASS  TRG_FUNCTION 
#
# Sample usage:
#   Ex1:  ./generate-tests.sh  Classify  60   112  Classify  classify
#	Ex2:  ./generate-tests.sh  01-Aliasing-ControlFlow-insecure  60  128   Main  process   
#	Ex1:  Run Classify for 60 seconds using 112 as the randomization seed 
#  

tolower(){
        echo $(echo $1 | tr '[:upper:]' '[:lower:]');
}

if [[ -z $2 ]]; then
	echo " Error: Missing parameter(s). Usage:"
	echo "  $0   CONTAINER JOBID "
	echo " Sample usage:"
	echo "   ./generate-tests.sh  23-Class-Example  171 "
	echo " Run test subject 23-Class-Example using 171 as the randomization seed"
	echo ""
  	exit 0
fi

CONTAINER=$1
RUNTIME=$2
JOBID=$3
TRG_CLS=$4
TRG_FUNCTION=$5

container=$(tolower "$CONTAINER")
container="$container-${JOBID}"
echo "Params: ${CONTAINER} ${JOBID} - ${container}"

date
mkdir -p evosuite-tests

docker build  -t evosuite  .
docker run --name ${container}  evosuite  /bin/bash  /evosuite/run.sh  \
     	${CONTAINER}  ${RUNTIME}  ${JOBID}   ${TRG_CLS} 

TRG="${container}:/evosuite/${CONTAINER}-${JOBID}"
echo "Target is: $TRG"
docker cp  ${TRG}   "./evosuite-tests/"
docker rm $container

python3 retrieve-functional-tests.py --trg_prj ${CONTAINER}  --trg_cls ${TRG_CLS} \
			--trg_function ${TRG_FUNCTION}  --jobid ${JOBID} 
date
