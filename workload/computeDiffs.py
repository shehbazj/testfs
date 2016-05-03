import sys
import re

BLOCK_SIZE = 64

if __name__ == "__main__":

    # Verify that the number of input arguments is correct.
    if len(sys.argv) != 3:
        print "Usage: python computeDiffs.py <input-file-1> <input-file-2>"
        sys.exit(-1)

    # Read the offsets from the first file and store them in a dictionary.
    with open(sys.argv[1]) as f_1:
        input_offsets_1 = ''.join(f_1.readlines()).strip()
        offsets_1 = re.findall(r"[\w']+", input_offsets_1)
        offsets_1 = set(offsets_1)

    # Read the offsets from the second file and store them in a dictionary.
    with open(sys.argv[2]) as f_2:
        input_offsets_2 = ''.join(f_2.readlines())
        offsets_2 = re.findall(r"[\w']+", input_offsets_2)
        offsets_2 = set(offsets_2)

    # Calculate which offsets exist only in the first file.
    print "Offsets not found in file {}...".format(sys.argv[2])
    for offset in sorted(offsets_1):
        if offset not in offsets_2:
            offset = int(offset)
            print "\t{} = {} * {} + {}".format(offset, BLOCK_SIZE, offset / BLOCK_SIZE, offset % BLOCK_SIZE)

    # Calculate which offsets exist only in the second file.
    print "\nOffsets not found in file {}...".format(sys.argv[1])
    for offset in sorted(offsets_2):
        if offset not in offsets_1:
            offset = int(offset)
            print "\t{} = {} * {} + {}".format(offset, BLOCK_SIZE, offset / BLOCK_SIZE, offset % BLOCK_SIZE)
