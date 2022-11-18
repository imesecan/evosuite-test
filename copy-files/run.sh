#!/bin/bash
# This script is not for direct usage. It is called by another script
# Usage:
#    ./run.sh  TEST_SUBJECT  RUNTIME_SECONDS  JOBID  TARGET_CLASS
# Sample usage:
#    ./run.sh  Sanitizers  60  135  "securibench micro sanitizers"  Sanitizers1
#

SRC=$1
SEC=$2
JOBID=$3
PREFIX=$4
TRG_CLS=$5

# SRC=Sanitizers
# SEC=60
# JOBID=182
# PREFIX="securibench micro sanitizers"
# TRG_CLS=Sanitizers1

HOME="/evosuite"
DST="${HOME}/${SRC}/src/main/java/"
JAR="evosuite-1.2.0.jar"
JAVAX="${HOME}/javax"
PFOLDER=
PACKAGE=

cp ${JAR} $DST
cp -r ${JAVAX}  ${DST}
cd $DST

for fld in $PREFIX; do
     PFOLDER="${PFOLDER}${fld}/"
     PACKAGE="${PACKAGE}${fld}."
done

echo "$PFOLDER $PACKAGE"
echo "Params: ${SRC} ${SEC} ${JOBID}  ${PREFIX}  ${TRG_CLS}"

mkdir -p evosuite-tests
cmd="javac -cp ${DST}  ${PFOLDER}${TRG_CLS}.java"
echo $cmd
$cmd

PRJ_CP=${DST}${PFOLDER}
cmd="-Xmx1G  -Xss1G  -jar ${JAR}  -projectCP ./  -class ${PACKAGE}${TRG_CLS}  -seed ${JOBID} \
     -Dsearch_budget=${SEC}  -Dstopping_condition=MaxTime "

echo "java $cmd"
java $cmd > ${HOME}/${SRC}.txt  2>&1

mv ${HOME}/${SRC}.txt  evosuite-report/*   evosuite-tests
mv evosuite-tests   ${HOME}/${SRC}-${JOBID}
