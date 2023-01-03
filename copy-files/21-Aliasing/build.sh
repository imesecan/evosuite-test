#!/bin/bash
# 
# Usage:
#    ./build.sh  
# Sample Usage:
#    ./build.sh  182
# Run the code using jobid 182 (seed is the same as jobid)
#

# Modifiye the sample input as needed
SAMPLE_INPUT=("3 42 15 3 18 2 9")

PREFIX=
TRG_CLS=Driver
DST="src/main/java/"
DEPENDENCE=
PACKAGE=

for fld in $PREFIX; do PACKAGE="${PACKAGE}${fld}."; done

mkdir -p targets
if [[ -n ${DEPENDENCE} ]]; then 
	cp ${DEPENDENCE} targets; 
	cd targets;
	jar xf ${DEPENDENCE}; 
	cd -
fi

targets=$(find ${DST}/ -name "*.java")
javac  -cp targets  -d targets  $targets
java -Xmx1G -Xss1G -cp targets  ${PACKAGE}${TRG_CLS} <<< "${SAMPLE_INPUT}"

# a=0
# alen=${#SAMPLE_INPUT[@]}
# while [[ $a -lt $alen ]]; 
# do
# 	val1=${SAMPLE_INPUT[${a}]}
# 	echo $val1
# 	java -Xmx1G -Xss1G -cp targets  ${PACKAGE}${TRG_CLS} <<< "${val1}"
# 	a=$((a+1))
# done
