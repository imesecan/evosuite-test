#!/bin/bash
#
# Sample usage 
#   ./GenTestRun.sh "M sec_1_1 sec_1_2 ... sec_1_M ... sec_2_1 sec_2_2 ... sec_2_M"
#   where 'M' is the number of secrets and 'low' is the low input
#	and there are 2 sets of secret inputs
#
# Sample run
#   ./GenTestRun.sh "4  36 78 42 247  42 138 155 217"
#
# Sample output
#   true true true false true true false false 
#

java org/leakreducer/GenTestDriver <<< $1
