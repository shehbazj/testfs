#!/usr/bin/env bash

# Verify that the input arguments are correct.
if [ "$#" -lt 1 ]; then
	echo "Wrong number of arguments!"
	echo "Usage: ./${0##*/} <backtrace>"
	exit -1
fi

# Prints the full path of the current directory.
#DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

for file in "$@"; do

taintLine=`head -1 $file`
taintValue=`echo $taintLine | cut -d'=' -f1`

tac $file > template/body.py

# Create a temporary Python file to process the generated tainted operations.
cat template/head.py template/body.py > template/$file.py
#echo "print $taintValue" >> template/$1.py

# Create a visualization using the dot language.
python template/$file.py
done
