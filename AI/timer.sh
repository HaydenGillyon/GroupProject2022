#!/bin/sh
time_start=`date '+%T%t%d_%h_06'`
echo "$time_start"

python ${1}

time_end=`date '+%T%t%d_%h_06'`
echo "$time_start"
echo "$time_end"

