#!/usr/bin/env bash

# Verify that the input arguments are correct.
if [ "$#" -ne 2 ]; then
	echo "Wrong number of arguments!"
	echo "Usage: ./${0##*/} <file-with-tainted-operations> <verbose-flag>"
	exit -1
fi

if [[ ("$2" != "true" && ("$2" != "false")) ]]; then
	echo -e "Unknown option: ${2}\nChoose one from {true, false}."
	exit -1
fi

# Prints the full path of the current directory.
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Create a temporary Python file to process the generated tainted operations.
cat $DIR/visualize/head.py $1 $DIR/visualize/tail.py > /tmp/visualize.py

# Create a visualization using the dot language.
if [ "$2" == "true" ]; then
	python /tmp/visualize.py --metadata --verbose
else
	python /tmp/visualize.py --metadata
fi
