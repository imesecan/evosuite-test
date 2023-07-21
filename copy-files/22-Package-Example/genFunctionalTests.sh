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
TRG_FUNCTION=calculate
TRG_CLS=Sanitizers1

Home=$(pwd)
DST="${Home}/src/main/java/"
JAR="evosuite-1.2.0.jar"
DEPENDENCE="Dependence.jar"
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
javac -d targets -cp "${HOME}/.m2/repository"  $targets; 

java -cp "targets" -Xmx1G -Xss1G -jar $JAR -projectCP "targets:${HOME}/.m2/repository" \
     -class ${PACKAGE}${TRG_CLS} -seed ${JOBID} -Dsearch_budget=$SEC \
     -Dstopping_condition=MaxTime > ${Home}/${SRC}.txt

TRG_FOLDER=${Home}/${SRC}-${JOBID}
mv ${Home}/${SRC}.txt  evosuite-report/*   evosuite-tests
mv evosuite-tests   ${TRG_FOLDER}
rm -rf evosuite-report targets ${JAR}

grep -HInr "${TRG_FUNCTION}" ${TRG_FOLDER}/ > tests${JOBID}.txt
mv tests${JOBID}.txt ${TRG_FOLDER}/
cd ${Home}
python3 get_tests.py --trg_function ${TRG_FUNCTION} --trg_project ${SRC} --jobid ${JOBID}
