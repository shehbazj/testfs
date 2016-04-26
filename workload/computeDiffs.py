import sys

if __name__ == "__main__":

    # Verify that the number of input arguments is correct.
    if len(sys.argv) != 3:
        print "Usage: python computeDiffs.py <input-file-1> <input-file-2>"
        sys.exit(-1)

    # Read the offsets from the first file and store them in a dictionary.
    with open(sys.argv[1]) as f_1:
        input_offsets_1 = ''.join(f_1.readlines()).strip()
        offsets_1 = input_offsets_1.split(",")
        offsets_1 = set(offsets_1)

    # Read the offsets from the second file and store them in a dictionary.
    with open(sys.argv[2]) as f_2:
        input_offsets_2 = ''.join(f_2.readlines()).strip()
        offsets_2 = input_offsets_2.split(",")
        offsets_2 = set(offsets_2)

    # Calculate which offsets exist only in the first file.
    print "Offsets not found in the 2nd file..."
    for offset in offsets_1:
        if offset not in offsets_2:
            print "\t{}".format(offset)

    # Calculate which offsets exist only in the second file.
    print "\nOffsets not found in the 1st file..."
    for offset in offsets_2:
        if offset not in offsets_1:
            print "\t{}".format(offset)