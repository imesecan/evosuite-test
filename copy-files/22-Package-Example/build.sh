#!/bin/bash
# 
# Usage:
#    ./build.sh  JOBID
# Sample Usage:
#    ./build.sh  182
# Run the code using jobid 182 (seed is the same as jobid)
#

PREFIX="securibench micro sanitizers"
TRG_CLS=Sanitizers1
SAMPLE_INPUT="1 2"
DST="src/main/java/"
DEPENDENCE="Dependence.jar"
PACKAGE=

for fld in $PREFIX; do PACKAGE="${PACKAGE}${fld}."; done

mkdir targets
cp ${DEPENDENCE} targets
cd targets; jar xf ${DEPENDENCE}; cd -

targets=$(find ${DST}/ -name "*.java")
javac  -cp targets  -d targets  $targets
java -Xmx1G -Xss1G -cp targets  ${PACKAGE}${TRG_CLS} <<< ${SAMPLE_INPUT}
