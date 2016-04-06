#!/usr/bin/env bash

# Verify that the input arguments are correct.
if [ "$#" -ne 1 ]; then
	echo "Wrong number of arguments!"
	echo "Usage: ./${0##*/} <file-with-tainted-operations>"
	exit -1
fi

# Prints the full path of the current directory.
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Create a temporary Python file to process the generated tainted operations.
cat $DIR/visualize/head.py $1 $DIR/visualize/tail.py > /tmp/visualize.py

# Create a visualization using the dot language.
python /tmp/visualize.py --metadata
