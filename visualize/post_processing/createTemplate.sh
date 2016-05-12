#!/usr/bin/env bash

# Verify that the input arguments are correct.
#if [ "$#" -lt 1 ]; then
#	echo "Wrong number of arguments!"
#	echo "Usage: ./${0##*/} <backtrace>"
#	exit -1
#fi

WORKING_DIR=`pwd`
SRC_DIR=`pwd`/backtrace
PREPROCESS_DIR=`pwd`/prenormalize
DEST_DIR=`pwd`/templates

if [ -d $PREPROCESS_DIR ]; then
	rm -rf $PREPROCESS_DIR
fi
mkdir $PREPROCESS_DIR

if [ -d $DEST_DIR ]; then
	rm -rf $DEST_DIR
fi
mkdir $DEST_DIR

# the variable replaces all constants with character 'C'
# useful for standardising templates
removeConstants=True

# Prints the full path of the current directory.
#DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $SRC_DIR
for file in *.back ; do
#file=`echo $f | cut -d'/' -f2`
echo "Processing $file"

taintLine=`head -1 $file`
taintValue=`echo $taintLine | cut -d'=' -f1`

#echo "global removeConstants" > template/body.py
rm $WORKING_DIR/templateBaseFunctions/body.py
echo "removeConstants=$removeConstants" >> $WORKING_DIR/templateBaseFunctions/body.py
tac $file >> $WORKING_DIR/templateBaseFunctions/body.py

# Create a temporary Python file to process the generated tainted operations.
cat $WORKING_DIR/templateBaseFunctions/head.py $WORKING_DIR/templateBaseFunctions/body.py >> $WORKING_DIR/prenormalize/$file.py
#echo "print $taintValue" >> template/$1.py

# 0 - place variables as constants.
# 1 - retain variables
blockNumber=`echo $file | cut -d'.' -f1`
python $WORKING_DIR/prenormalize/$file.py > $WORKING_DIR/templates/$file.template
$WORKING_DIR/evalTemplate.sh $file $blockNumber
done
