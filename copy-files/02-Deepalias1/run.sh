#!/bin/bash
# 
# Usage:
#    ./build.sh  
# Sample Usage:
#    ./build.sh  182
# Run the code using jobid 182 (seed is the same as jobid)
#

# Modifiye the sample input as needed
SAMPLE_INPUT=("-8" "3" "2")

PREFIX=""
TRG_CLS=EvoDriver
DST="src/main/java/"
DEPENDENCE=
PACKAGE=
for fld in $PREFIX; do PACKAGE="${PACKAGE}${fld}."; done

a=0
alen=${#SAMPLE_INPUT[@]}
while [ $a -lt $alen ]; 
do
	val1=${SAMPLE_INPUT[${a}]}
	java -Xmx1G -Xss1G -cp targets  ${PACKAGE}${TRG_CLS} <<< "${val1}"
	a=$((a+1))
done
