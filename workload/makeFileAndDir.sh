#!/bin/bash

usage="\n\t./makeFileAndDir.sh <numDir> <numFile>\n\n\tgenerates touch and mkdir commands to create files and directories"

if [[ $# -ne 2 ]]; then
	echo -e "$usage";
	exit 1
fi

numDir=$1
numFile=$2

# create all files and directories in the root directory itself
if [[ $numDir -le 3 || $numFile -le 3 ]]; then

	# create directories
	for i in `seq 1 $numDir`; do
		echo "mkdir dir$i"
	done

	# create files
	for i in `seq 1 $numFile`; do
		echo "touch file$i"
	done
else
	# create two level directory with 1 file i.e. dir1/dir1_2/file1
	echo -e "mkdir dir1\ncd dir1\nmkdir dir1_2\ncd dir1_2\ntouch file1\ncd ..\ncd .."

	# create 1 level directory with 1 directory i.e. dir2/dir2_2
	echo -e "mkdir dir2\ncd dir2\nmkdir dir2_2\ncd .."

	# create 1 level directory with 1 file i.e. dir3/file2
	echo -e "mkdir dir3\ncd dir3\ntouch file2\ncd .."

	# create all other files and directories in / directory
	for i in `seq 3 $numFile`; do
		echo "touch file$i"
	done

	for i in `seq 4 $numDir`; do
		echo "mkdir dir$i"
	done

fi

exit 0


