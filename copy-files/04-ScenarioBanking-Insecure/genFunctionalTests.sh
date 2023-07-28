#!/bin/bash
# 
# Usage:
#    ./genFunctionalTests.sh  SEC  JOBID  TRG_CLS  PREFIX
# Sample Usage:
#    ./genFunctionalTests.sh  60  182   Main  "org leakreducer"
#
# Run the code using jobid 182 (seed is the same as jobid)
#

SEC=$1				# runtime in seconds
JOBID=$2			# unique id to describe this job
TRG_CLS=$3			# target class name
PREFIX=$4			# prefix for package 

SRC=${PWD##*/}
re='^[0-9]+$'
if ! [[ $JOBID =~ $re ]] ; then
     printf "WARNING: JOBID not set, exiting!\n Usage:\n   $0  JOBID\n"
     printf " Usage:\n   $0  SEC  JOBID  TRG_CLS\n"
     printf " Sample:\n   $0  60  182  Main\n"
     
     exit 1
fi

Home=$(pwd)
DST="${Home}/src/main/java/"
JAR="evosuite-1.2.0.jar"
DEPENDENCE=
PACKAGE=
for fld in $PREFIX; do PACKAGE="${PACKAGE}${fld}."; done
echo "Params: ${SRC} ${SEC} ${JOBID}  ${PREFIX}  ${TRG_CLS}"
cp ../${JAR} $DST

if [[ -n ${DEPENDENCE} ]]; then
     cd ${HOME}/.m2/repository
     jar xf /evosuite/${SRC}/${DEPENDENCE}
fi
cd $DST

mkdir -p evosuite-tests
rm -rf targets
targets=$(find ./ -name "*.java")

javac -d targets $targets;
java -cp "targets" -Xmx1G -Xss1G -jar $JAR -projectCP "targets:${HOME}/.m2/repository" \
     -class ${PACKAGE}${TRG_CLS} -seed ${JOBID} -Dsearch_budget=$SEC \
     -Dstopping_condition=MaxTime > ${Home}/${SRC}.txt

TRG_FOLDER=${Home}/${SRC}-${JOBID}
mv ${Home}/${SRC}.txt  evosuite-report/*   evosuite-tests
mv evosuite-tests   ${TRG_FOLDER}
rm -rf evosuite-report targets ${JAR}
