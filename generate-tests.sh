#!/bin/bash
#
# Usage:
#   ./generate-tests.sh  CONTAINER JOBID 
#
# Sample usage:
#     ./generate-tests.sh  23-Class-Example  171
#   Run test subject 23-Class-Example using 171 as the randomization seed 
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
JOBID=$2

container=$(tolower "$CONTAINER")
container="$container-${JOBID}"
echo "Params: ${CONTAINER} ${JOBID} - ${container}"

date
mkdir -p evosuite-tests

docker build  -t evosuite  .
docker run --name ${container}  evosuite  /bin/bash  /evosuite/run.sh  \
     	${CONTAINER} ${JOBID}

TRG="${container}:/evosuite/${CONTAINER}-${JOBID}"
echo "Target is: $TRG"
docker cp  ${TRG}   "./evosuite-tests/"
docker rm $container
date
