# given a block ID number and a trace file, this script gives the backtrace of
# the taint ids that lead to generation of the block, until it reaches a block
# or a t0 taint.


if [[ $# -ne 1 ]]; then
	echo "Usage : ./backtrace.sh trace_file <block_num>"
	exit
fi

# remove existing scratch_space directory

if [ -d scratch_space ]; then
	rm -rf scratch_space
fi

trace_file=$1

if [ ! -f $trace_file ]; then
	echo "File " $trace_file "does not exist"
	exit 
else
	mkdir scratch_space
	cp $trace_file scratch_space
	cd scratch_space
fi
blockFile=$trace_file."block"

cat $trace_file | grep "B(" > $blockFile
#cat $blockFile







