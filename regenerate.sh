#!/bin/bash
#three parameters required: 1.txt file 2.image path root 3.video path root
txtfile=$1
imageroot=$2
videoroot=$3
echo ${#imageroot}
mp4=".mp4"
ts=".ts"
cat $1 | while read line
do 
path=${line%%has*}
folder=${path:${#imageroot}:${#path}}
resume=${line##*images}
video=$folder
echo $videoroot$folder
#if [ "$resume" == "" ]; then
#echo "empty"
#else
#echo $resume
#fi
 
done
