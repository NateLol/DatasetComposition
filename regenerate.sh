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
path=${line%%" has"*}
resume=${line##*images}

folder=${path:${#imageroot}:${#path}}
video=$videoroot$folder
if [ -f "$video$mp4" ]; then
	target=$video$mp4
	echo $target
elif [ -f "$video$ts" ]; then
	target=$video$ts
	echo $target
else
	echo "No Such file"$video
	exit 0
fi

if [ "$resume" == "" ]; then
	python 6_fps.py --video "$target" --folder "$path" --stride 1
else
	python 7_fps_part.py --video "$target" --folder "$path" --resume $resume
fi

done
