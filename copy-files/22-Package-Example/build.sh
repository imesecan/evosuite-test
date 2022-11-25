#!/bin/bash
# 
# Usage:
#    ./build.sh  JOBID
# Sample Usage:
#    ./build.sh  182
# Run the code using jobid 182 (seed is the same as jobid)
#

JOBID=$1

re='^[0-9]+$'
if ! [[ $JOBID =~ $re ]] ; then
     printf "WARNING: JOBID not set, exiting!\n Usage:\n   $0  JOBID\n"
     printf " Sample Usage:\n   $0  182\n"
     
     exit 1
fi

SRC=${PWD##*/}
SEC=60
PREFIX="securibench micro sanitizers"
TRG_CLS=Sanitizers1

Home=$(pwd)
DST="${Home}/src/main/java/"
JAR="evosuite-1.2.0.jar"
DEPENDENCE="Dependence.jar"
PFOLDER=
PACKAGE=

cp *.jar $DST
cd $DST

for fld in $PREFIX; do
     PFOLDER="${PFOLDER}${fld}/"
     PACKAGE="${PACKAGE}${fld}."
done

echo "$PFOLDER $PACKAGE"
echo "Params: ${SRC} ${SEC} ${JOBID}  ${PREFIX}  ${TRG_CLS}"

mkdir -p evosuite-tests
rm -rf targets
targets=$(find ./ -name "*.java")
javac -d targets -cp "${DST}${DEPENDENCE}"  $targets; 
cd targets
echo "Class-Path: ./${DEPENDENCE}" > Manifest.txt
targets=$(find . -name "*.class")
jar cfem ../${TRG_CLS}.jar ${PACKAGE}${TRG_CLS} Manifest.txt $targets
cd ..
java -Xmx1G -Xss1G -jar $JAR -projectCP "./:./${TRG_CLS}.jar" -class ${PACKAGE}${TRG_CLS} -seed ${JOBID} \
     -Dsearch_budget=$SEC -Dstopping_condition=MaxTime > ${Home}/${SRC}.txt

mv ${Home}/${SRC}.txt  evosuite-report/*   evosuite-tests
mv evosuite-tests   ${Home}/${SRC}-${JOBID}
