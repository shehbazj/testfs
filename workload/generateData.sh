#!/bin/bash

usage="\n\t./generateData <numDir> <numFile> <numDataBlocks> <0|1>\n
	0 - all files are created equally
	1 - binary sized file distribution\n
	default is equal sized file distribution\n
	generates data for files and directories created using ./createFileAndDir.sh\n"

if [[ $# -lt 3 ]]; then
	echo -e "$usage";
	exit 1
fi

numDir=$1
numFile=$2
numBlocks=$3

# if no arg specified, use equal file sized distribution
fileDistribution=${4:-0}

echo "FILE DISTRIBUTION $fileDistribution"
TOTAL_BYTES=$(($numBlocks * 64))
for i in `seq 1 $TOTAL_BYTES`; do
	byte_string="$byte_string$((i%10))"
done

# echo "TOTAL BYTES = $TOTAL_BYTES"
# echo $byte_string

avg_file_size=$((TOTAL_BYTES / $numFile))

if [[ $numDir -le 3 || $numFile -le 3 ]]; then
	# all files and directories are in root directory.
	# write TOTAL_BYTES / numFile data to top 2 files.
	# create binary distribution of data for other files

	for i in `seq 1 $numFile`; do
		echo -e "write file$i \c" 
		begin=$(($((i-1)) * $avg_file_size))
		end=$((begin+$avg_file_size))
		echo ${byte_string:begin:end} 
	done
else
	# write data for two level directory with 1 file i.e. dir1/dir1_2/file1
	begin=0
	end=$avg_file_size
	echo -e "cd dir1\ncd dir1_2\nwrite file1 ${byte_string:begin:end}\ncd ..\ncd .."

	# write data to 1 level directory with 1 file i.e. dir3/file2
	begin=$((end+1))
	end=$((begin+$avg_file_size))
	echo -e "cd dir3\nwrite file2 ${byte_string:begin:$((end-$begin))}\ncd .."

	REMAINING_BYTES=$((TOTAL_BYTES - $((avg_file_size *2))))

	# write data to rest of the files
	if [[ $fileDistribution -eq 0 ]]; then
		# echo "EQUAL SIZED FILES"
		# equal size files
		for i in `seq 3 $numFile`; do
			begin=$((end+1))	
			end=$((begin+$avg_file_size))
			echo "write file$i ${byte_string:begin:avg_file_size}"
		done
	else
		# binary distribution sized files
		# echo "BINARY DISTRIBUTION SIZED FILES"
		for i in `seq 3 $numFile`; do
			begin=$((begin+len+1))
			if [[ $REMAINING_BYTES > $(( 2 * $numFile)) ]]; then
				len=$((REMAINING_BYTES / 2))
				REMAINING_BYTES=$((REMAINING_BYTES / 2))
			else
				len=$((REMAINING_BYTES / $((numfile -$i ))))
				REMAINING_BYTES=$((REMAINING_BYTES - $len))
			fi
			echo "write file$i ${byte_string:begin:len}"
		done
	fi
fi

exit 0
