#!/bin/bash
# This script is not for direct usage. It is called by another script
# Usage:
#    ./build.sh 
#

SRC=${PWD##*/}
Home=$(pwd)
DST="${Home}/src/main/java/"
DEPENDENCE=

cd $DST
echo "Params: ${SRC} $DST"

rm -rf targets
targets=$(find ./ -name "*.java")
echo $targets;
javac -d targets -cp "./${DEPENDENCE}"  $targets; 
cd targets
echo "Class-Path: ./${DEPENDENCE}"  >  Manifest.txt
targets=$(find . -name "*.class")
jar cfm ${Home}/${SRC}.jar Manifest.txt $targets
