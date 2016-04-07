import sys
import argparse

TOTAL_BLOCKS = 704
BLOCK_SIZE = 64

parser = argparse.ArgumentParser(description='Print disk\'s layout.')
parser.add_argument('--all', dest='PRINT_ALL', const=True, default=False,
                    nargs='?', help='Print all disk blocks.')
parser.add_argument('--verbose', dest='VERBOSE', const=True, default=False,
                    nargs='?', help='Print debug information.')

args = parser.parse_args()


class Metadata(object):
    def __init__(self):
        self.datatypes = dict()
        self.bytes = dict()
        self.assigned_colours = dict()
        self.available_colours = ["green", "yellow", "orange", "purple", "cyan", "red"]
        self.max_block_nr = 0

    def add_entry(self, offset, size, type):
        if args.VERBOSE:
            print "[DEBUG]: Invoking add_entry({}, {}, {})".format(offset, size, type)

        if type not in self.datatypes:
            if len(self.available_colours) == 0:
                print "[ERROR]: There are no new colours available..."
                sys.exit(-1)
            else:
                self.datatypes[type] = self.available_colours.pop(0)
                self.assigned_colours[type] = self.datatypes[type]

        colour = self.datatypes[type]
        for byte in xrange(offset, offset + size):
            if byte in self.bytes:
                current_colour = self.bytes[byte]
                if args.VERBOSE:
                    print "[WARN]: Byte {} has already been assigned {} colour.".format(byte, current_colour)
            else:
                self.bytes[byte] = colour

        block_nr = offset / BLOCK_SIZE;
        if block_nr > self.max_block_nr:
            self.max_block_nr = block_nr

    def print_bytes(self):
        return "|".join("<b{}>".format(i) for i in range(BLOCK_SIZE))

    def generate_graph(self):
        print "digraph {"
        print "\trankdir=TB;"

        print "\tsubgraph legend {"
        print "\t\trank = sink"
        print "\t\tLegend [shape = none, margin = 0, label = <"
        print "\t\t<table border=\"1\" cellpadding=\"5\" cellspacing=\"5\" cellborder=\"0\">"

        for type, colour in self.assigned_colours.iteritems():
            print "\t\t\t<tr>"
            print "\t\t\t\t<td>{}</td>".format(type)
            print "\t\t\t\t<td bgcolor=\"{}\"></td>".format(colour)
            print "\t\t\t</tr>"
        print "\t\t</table>>];"
        print "\t}\n"

        # print "\t\ttype [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">"
        # for type, colour in self.assigned_colours.iteritems():
        #     print "\t\t\t<tr><td>{}</td></tr>".format(type)
        # print "\t\t</table>>];"

        if args.PRINT_ALL:
            block_limit = BLOCK_SIZE * TOTAL_BLOCKS
        else:
            block_limit = BLOCK_SIZE * (self.max_block_nr + 1)

        for nr in xrange(0, block_limit, BLOCK_SIZE):
            block_nr = nr / BLOCK_SIZE

            print "\tn{} [".format(block_nr)
            print "\t\tshape = none\n\t\tlabel = <<table border = \"0\" cellspacing = \"0\">"
            print "\t\t\t<tr>"
            print "\t\t\t\t<td border=\"1\" bgcolor=\"grey\">Block {}</td>".format(block_nr)

            for i in xrange(0, BLOCK_SIZE):
                disk_offset = (block_nr * BLOCK_SIZE) + i
                if disk_offset in self.bytes:
                    colour = self.bytes[disk_offset]
                else:
                    colour = "grey"

                print "\t\t\t\t<td port=\"b{}\" border=\"1\" bgcolor=\"{}\"></td>".format(i, colour)

            print "\t\t\t</tr>"
            print "\t\t</table>>"
            print "\t];"


        print "}"


if __name__ == "__main__":
    metadata = Metadata()

    for input_line in sys.stdin:
        tokens = input_line.split(" ")

        tokens[0] = int(tokens[0])
        tokens[1] = int(tokens[1])
        type = ' '.join(tokens[2:]).strip()

        metadata.add_entry(tokens[0], tokens[1], type)

    # Generate the graph in dot language.
    metadata.generate_graph()
