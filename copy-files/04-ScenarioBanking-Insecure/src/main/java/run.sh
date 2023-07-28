#!/bin/bash
#
# Sample usage for Classify.java
#   ./run.sh "N low_1 high_1 low_2 high_2 ... low_N high_N "
# Sample run
#   ./run.sh "3 137 135 42 79 86 255"
# Sample output
#   135 2 255
#

java org/leakreducer/Driver <<< $1
