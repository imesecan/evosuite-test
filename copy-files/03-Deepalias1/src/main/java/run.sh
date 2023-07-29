#!/bin/bash
#
# Sample usage for Classify.java
#   ./run.sh "N high_1 high_2 ... high_N "
# Sample run
#   ./run.sh "3 135 78 255"
# Sample output
#   false true false 
#

java org/leakreducer/Driver <<< $1
