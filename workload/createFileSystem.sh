#!/bin/bash

usage="\n\t./createFileSystem.sh <percentage_full> <distribution>
	\n percentage_full 25 50 75
	\n distribution 0 - all files created are equal in size
	\n		1 - file sizes have binary distribution
	\n\tgenerates workload for file system to occupy percent_full inodes and data blocks\n"

if [[ $# -ne 2 ]]; then
	echo -e "$usage";
	exit 1
fi

INODE=128
DBLOCK=512

percent=$1
distribution=$2
numInode=$(($((percent * $INODE))/100))
numDataBlock=$(($((percent * $DBLOCK))/100))

numDir=$((numInode / 2))
numFile=$((numInode / 2))

rm workload.$percent
# echo "percent $percent, numInode = $numInode, numDataBlock = $numDataBlock"
./makeFileAndDir.sh $numDir $numFile >> workload.$percent
./generateData.sh $numDir $numFile $numDataBlock $distribution >> workload.$percent

exit 0
