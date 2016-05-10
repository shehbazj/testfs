#!/usr/bin/env bash

# Verify that the input arguments are correct.
if [ "$#" -lt 1 ]; then
	echo "Wrong number of arguments!"
	echo "Usage: ./${0##*/} <backtrace>"
	exit -1
fi

if [ -d templates ]; then
	rm -rf templates
fi
mkdir templates

if [ -d classifier ]; then
	rm -rf classifier
fi
mkdir classifier

# the variable replaces all constants with character 'C'
# useful for standardising templates
removeConstants=True

# Prints the full path of the current directory.
#DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

for file in "$@"; do
echo "Processing $file"

taintLine=`head -1 $file`
taintValue=`echo $taintLine | cut -d'=' -f1`

#echo "global removeConstants" > template/body.py
rm template/body.py
echo "removeConstants=$removeConstants" >> template/body.py
tac $file >> template/body.py

# Create a temporary Python file to process the generated tainted operations.
cat template/head.py template/body.py >> templates/$file.py
#echo "print $taintValue" >> template/$1.py

# 0 - place variables as constants.
# 1 - retain variables
blockNumber=`echo $file | cut -d'.' -f1`
python templates/$file.py > classifier/$file.template
head -n -1 classifier/$file.template > classifier/all_lines_except_last
cksum classifier/all_lines_except_last | cut -d' ' -f1 >> classifier/$blockNumber
rm classifier/$file.template
done

rm classifier/all_lines_except_last
