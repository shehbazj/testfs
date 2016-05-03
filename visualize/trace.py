import argparse
import re

if __name__ == "__main__":
    """ Main Start """

    parser = argparse.ArgumentParser()
    parser.add_argument('taint_val', type=str, help="TaintID to trace: ex. 1234")
    parser.add_argument('trace_file', type=str, help="The path to the trace file.")
    parser.add_argument('-b', action='store_true')
    args = parser.parse_args()

    with open(args.trace_file, 'r') as f:

        relevant_lines = []
        flag = None
	printFunctionNames = None
	#printFunctionNames = True

        # Forward pass
        if args.b:
            taint_str = 't' + args.taint_val + '='
            relevant = set([taint_str])

            for line in reversed(f.readlines()):
                if line[0] == '#' and printFunctionNames != True:
                    continue
                line = line.strip()

                # Match
                curset = set(re.findall(r"t[0-9]+=", line))
                if relevant.intersection(curset) and len(curset):

                    cur = re.findall(r"t[0-9]+", line)
                    sol = []
                    for taint in cur:
                        sol.append(taint + '=')

                    relevant |= set(sol)
                    relevant_lines.append(line)
                    if printFunctionNames == True:
                        flag = True
		
		if printFunctionNames == True:
                    if line.endswith("()") and flag:
                        relevant_lines.append(line)
                        flag = False

            for line in relevant_lines:
                print line

        # all
        else:
            taint_str = 't' + args.taint_val
            relevant = set([taint_str])

            for line in reversed(f.readlines()):
                if line[0] == '#':
                    continue
                line = line.strip()

                # Match
                curset = set(re.findall(r"t[0-9]+", line))
                if relevant.intersection(curset) and len(curset):
                    relevant_lines.append(line)

            for line in reversed(relevant_lines):
                print line
