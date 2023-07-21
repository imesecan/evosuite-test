#!/bin/bash
#
# Sample usage 
#   ./run.sh "secret_1 side2_1 side3_1 secret_2 side2_2 side3_2 ..."
# Sample run
#   ./run.sh "2 3 4 3 3 4"
# Sample output
#   1 3
#

PREFIX="securibench micro sanitizers"
TRG_CLS=Sanitizers1
N=$1
SAMPLE_INPUT=$2

PACKAGE=
for fld in $PREFIX; do PACKAGE="${PACKAGE}${fld}."; done

for ((k=0; k<N; k++)) do 
	java -Xmx1G -Xss1G -cp targets  ${PACKAGE}${TRG_CLS} <<< ${SAMPLE_INPUT}
done
