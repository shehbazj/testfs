import sys
import argparse

parser = argparse.ArgumentParser(description='Generate statistics for a TestFS workload.')
parser.add_argument('--verbose', dest='VERBOSE', const=True, default=False,
                    nargs='?', help='Print debug information.')

args = parser.parse_args()

BLOCK_SIZE = 64

total_bytes_per_dir_or_file = dict()

if __name__ == "__main__":

    # Initialize the current directory to be the root.
    current_directory = "/"

    # Initialize the full path to the parent directory.
    path_to_parent = "/"

    # Maintain a stack of directory names, in order to calculate the
    # current directory in case of 'cd' operations.
    directory_stack = []

    # 9 + len("./") + 9 + len("../")
    total_bytes_per_dir_or_file[current_directory] = 23

    for input_line in sys.stdin:
        # Split the input line and strip the '\n' character
        # from the last argument.
        arguments = input_line.split(" ")
        arguments[-1] = arguments[-1].strip()
        cmd = arguments[0]

        if cmd == "write":
            # Calculate the absolute path to the specified file.
            path_to_file = path_to_parent + arguments[1]

            # Make sure that the file is already stored inside the dictionary.
            # A file must have already been created ('touch'), in order for the
            # write operation to proceed.
            assert (path_to_file in total_bytes_per_dir_or_file)

            # The 'write' command always writes some bytes at the beginning of the
            # file, i.e., it does not append new data.
            current_len = total_bytes_per_dir_or_file[path_to_file]
            new_length = max(current_len, len(arguments[2]))
            total_bytes_per_dir_or_file[path_to_file] = new_length

        elif cmd == "touch":
            # 'Touch' supports multiple file names.
            for i in xrange(1, len(arguments)):
                # Calculate the absolute path to the specified file.
                path_to_file = path_to_parent + arguments[i]

                # Make sure that the specified name does not already exist.
                assert(path_to_file not in total_bytes_per_dir_or_file)
                total_bytes_per_dir_or_file[path_to_file] = 0

                # Make sure that the parent directory already exists.
                assert(path_to_parent in total_bytes_per_dir_or_file)

                # Every file creation results in a new directory entry.
                # len(d_entry) = 9 + len(filename).
                total = total_bytes_per_dir_or_file[path_to_parent]
                total += (9 + len(arguments[i]))
                total_bytes_per_dir_or_file[path_to_parent] = total

        elif cmd == "mkdir":
            # Make sure that the directory name ends with '/'.
            if arguments[1][-1] != '/':
                arguments[1] += '/'

            # Verify that the specified directory does not already exist.
            path_to_file = path_to_parent + arguments[1]
            assert (path_to_file not in total_bytes_per_dir_or_file)

            # 9 + len("./") + 9 + len("../")
            total_bytes_per_dir_or_file[path_to_file] = 23

            # Verify that the parent directory has already been created.
            assert (path_to_parent in total_bytes_per_dir_or_file)
            total = total_bytes_per_dir_or_file[path_to_parent]

            # len(d_entry) = 9 + len(filename).
            total += (8 + len(arguments[1]))
            total_bytes_per_dir_or_file[path_to_parent] = total

        elif cmd == "cd":
            if arguments[1] == ".." or arguments[1] == "../":
                # The current directory will be equal to the directory
                # that was inserted last into the stack.
                current_directory = directory_stack.pop()
            else:
                # Make sure that the directory name ends with '/'.
                if arguments[1][-1] != '/':
                    arguments[1] += '/'

                # Make sure that the directory exists.
                path_to_file = path_to_parent + arguments[1]
                assert(path_to_file in total_bytes_per_dir_or_file)

                # Add the current directory to the directory stack.
                directory_stack.append(current_directory)

                # Mark the specified directory as the current directory.
                current_directory = arguments[1]

            # Update the absolute path to the parent directory.
            path_to_parent = ''.join(directory_stack) + current_directory

        else:
            print "Unknown command: {}\nExiting...".format(cmd)
            sys.exit(-1)

    # The number of inodes equals to the number of files and directories (keys)
    # stored inside the directory.
    total_inodes = len(total_bytes_per_dir_or_file.keys())

    # The superblock contains 5 integer fields that are used as
    # on-disk pointers.
    total_direct_pointers = 5
    total_indirect_pointers = 0

    for _, size in total_bytes_per_dir_or_file.iteritems():
        # If the size of the file is larger than 4 * BLOCK_SIZE
        # then, an indirect block will be used.
        if size > (4 * BLOCK_SIZE):
            total_indirect_pointers += 1

        # Count one direct pointer per BLOCK_SIZE bytes.
        for i in xrange(0, size, BLOCK_SIZE):
            total_direct_pointers += 1

    # There is at least direct pointer for the '/' (root) directory.
    assert(total_direct_pointers > 5)

    print "Statistics:"
    if args.VERBOSE:
        print "  -- Total bytes: {}".format(total_bytes_per_dir_or_file)

    print "  -- Total inodes: {}".format(total_inodes)
    print "  -- Total direct pointers: {}".format(total_direct_pointers)
    print "  -- Total indirect pointers: {}".format(total_indirect_pointers)