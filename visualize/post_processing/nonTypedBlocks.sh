# Non Typed Blocks - gives us a list of blocks whose sub-elements are not accessed

echo "Usage ./nonTypedBlocks.sh <taintFile>"

TAINT_FILE=${1:-/tmp/testfs.py}

rm blockTaints operations

cat $TAINT_FILE | grep "B(64," | cut -d"=" -f1 >> blockTaints

cat $TAINT_FILE | cut -d"=" -f2 >> operations

while read operations ;do
	while read taint; do
#		echo $operation $taint
#		#echo $taint
		blockTaintStr=$taint"["
#		echo $blockTaintStr
		if [[ $operations != *$blockTaintStr* ]]; then
			echo "mismatch"
		else
			echo "$taint" > 	
		fi
	done < blockTaints
done < operations
