# Non Typed Blocks - gives us a list of blocks whose sub-elements are not accessed

echo "Usage ./nonTypedBlocks.sh <taintFile>"

TAINT_FILE=${1:-/tmp/testfs.py}

rm blockTaints operations

cat $TAINT_FILE | grep "B(64," | cut -d"=" -f1 >> blockTaints

cat $TAINT_FILE | grep "B(64," | cut -d"," -f2 >> blockNumbers

paste -d" " blockTaints blockNumbers > TaintBlockFile

declare -A taintBlockHash

while read line; do
	taint=`echo $line | cut -d" " -f1`
	blockNum=`echo $line | cut -d" " -f2`
	taintBlockHash[$taint]=$blockNum
done < TaintBlockFile

cat $TAINT_FILE | cut -d"=" -f2 >> operations

while read taint; do
	blockTaintStr=$taint"["
	flag=1
	while read operations; do
		if [[ $operations == *$blockTaintStr* ]]; then
			echo "$operations contains $blockTaintStr"
			flag=0
			#break	
		fi
	done < operations
	if [[ $flag -eq 0 ]]; then
		echo ${taintBlockHash[$taint]}
	else
		echo "flag is false"
	fi
done < blockTaints