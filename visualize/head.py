import sys
import collections
import argparse

parser = argparse.ArgumentParser(description='Calculate output graph.')
parser.add_argument('--metadata', dest='PRINT_METADATA', const=True, default=False,
                    nargs='?', help='Print metadata.')

args = parser.parse_args()

pointerList = collections.defaultdict(list)
pointerSet = set()
valueSet = collections.defaultdict(int)
abstractDataSet = set()
nameSet = set()


class Base(object):
    def __init__(self, taintID = ""):
        self.size = 1
        self.byte_sources = {}
        self.taintID = taintID

    def __getitem__(self, byte):
        self.size = max(self.size, byte + 1)
        return Select(self, byte)

    def __setitem__(self, byte, val):
        self.byte_sources[byte] = val

    def getName(self):
        return self.__class__.__name__

    def Label(self):
        return "n{}".format(id(self))

    def PrintByteSources(self, next, edges):
        for i, s in self.byte_sources.items():
            next.add(s)
            edges.add("{}:b{} -> {} [ label=\"t{}\" ];".format(self.Label(), i, s.Label(), s.taintID))

    def _bytes(self):
        return "|".join("<b{}>".format(i) for i in range(self.size))

    def markPointer(self, byte, block_number):
        pass

    def markPointers(self, block_number):
        pass

    def getByte(self, byte):
        return self.byte_sources[byte]


class Select(Base):
    def __init__(self, parent, byte):
        Base.__init__(self, parent.taintID)
        self.parent = parent
        self.byte = byte

    def markPointers(self, block_number):
        self.parent.markPointer(self.byte, block_number)

    def Print(self, next, edges):
        next.add(self.parent)

    def Label(self):
        return "{}:b{}".format(self.parent.Label(), self.byte)


class V(Base):
    def __init__(self, val, taintID):
        Base.__init__(self, taintID)
        self.val = val
        self.usedAsPointer = False

    def markPointers(self, block_number):
        assert self.val == block_number
        self.usedAsPointer = True

    def Print(self, next, edges):
        print "{} [label=\"{{{{{}}}|{}}}\"];".format(self.Label(), self._bytes(), self.val)


class A(Base):
    def __init__(self, op, a, b, taintID):
        Base.__init__(self, taintID)
        self.op = op
        self.left = a
        self.right = b

        # if isinstance(self.left, V):
        #     print "[Object {}]: Found value: {}".format(self.taintID, self.left.taintID)
        # elif isinstance(self.right, V):
        #     print "[Object {}]: Found value: {}".format(self.taintID, self.right.taintID)

    def markPointers(self, block_number):
        self.left.markPointers(block_number)
        self.right.markPointers(block_number)

    def Print(self, next, edges):
        if isinstance(self.left, V):
            LL = str(self.left.val)
        else:
            next.add(self.left)
            LL = "<left>"
            edges.add("{}:left -> {} [ label=\"t{}\" ];".format(self.Label(), self.left.Label(), self.left.taintID))

        if isinstance(self.right, V):
            RL = str(self.right.val)
        else:
            next.add(self.right)
            RL = "<right>"
            edges.add("{}:right -> {} [ label=\"t{}\" ];".format(self.Label(), self.right.Label(), self.right.taintID))

        print "{} [color=blue label=\"{{ {{ {} }} | {{ {} | t{} }} | {{{}|{}}} }}\"];".format(
                self.Label(), self._bytes(), self.op, self.taintID, LL, RL)


class O(Base):
    def __init__(self, taintID, *bytes):
        Base.__init__(self, taintID)
        self.bytes = bytes
        self.size = len(self.bytes)

        # if self.size > 0:
        #     if isinstance(self.__getitem__(0), V):
        #         print "[Object {}]: Found value: {}".format(self.taintID, self.__getitem__(0).taintID)

    def markPointers(self, block_number):
        for i in xrange(0, self.size):
            self.__getitem__(i).markPointers(block_number)

    def __getitem__(self, byte):
        self.size = max(self.size, byte + 1)
        if byte < len(self.bytes):
            return self.bytes[byte]
        else:
            return Select(self, byte)

    def Print(self, next, edges):
        print "{} [label=\"{{{{}}|{{{}}}}}\"];".format(self.Label(), self._bytes())
        for i, b in enumerate(self.bytes):
            next.add(b)
            edges.add("{}:b{} -> {} [ label=\"t{}\" ];".format(self.Label(), i, b.Label(), b.taintID))


class B(Base):
    BLOCKS = []

    def __init__(self, size, nr, block_size, block_nr, taintID):
        Base.__init__(self, taintID)
        self.size = size
        self.nr = nr
        self.block_size = block_size
        self.block_nr = block_nr
        self.BLOCKS.append(self)

        if not isinstance(self.block_size, V):
            block_size.markPointers(self.nr)

        if not isinstance(self.block_nr, V):
            block_nr.markPointers(self.nr)

        # if isinstance(self.block_size, V):
        #     print "[Object {}]: Found value: {}".format(self.taintID, self.block_size.taintID)
        # elif isinstance(self.block_nr, V):
        #     print "[Object {}]: Found value: {}".format(self.taintID, self.block_nr.taintID)

    def __setitem__(self, byte, val):
        Base.__setitem__(self, byte, val)

        if isinstance(val.parent, V):
            valueSet[(self.nr * self.size) + byte] = val.parent.val

        if isinstance(val.parent, D):
            # print "Inside block {} with offset {} and value {} and {}".format(self.nr, byte, val.taintID, val.parent.getByte(byte).parent.taintID)
            if val.parent.getByte(val.byte).parent.getName() == 'N':
                nameSet.add((self.nr * self.size) + byte)
            else:
                abstractDataSet.add((self.nr * self.size) + byte)

    def markPointer(self, byte, block_number):
        disk_offset = (self.size * self.nr) + byte
        pointerList[block_number].append(disk_offset)
        pointerSet.add(disk_offset)

    def Print(self, next, edges):
        print "{} [rank=max fillcolor=grey style=filled label=\"{{{{{}}}|{{<size>size = {} | <nr>nr = {} | <tid>tid = {}}}}}\"];" \
            .format(self.Label(), self._bytes(), self.size, self.nr, self.taintID)

        if not isinstance(self.block_size, V):
            next.add(self.block_size)
            edges.add("{}:size -> {} [ label=\"t{}\" ];"
                      .format(self.Label(), self.block_size.Label(), self.block_size.taintID))

        if not isinstance(self.block_nr, V):
            next.add(self.block_nr)
            edges.add("{}:nr -> {} [ label=\"t{}\" ];"
                      .format(self.Label(), self.block_nr.Label(),self.block_nr.taintID))


class NT(Base):
    def __init__(self, taintID):
        Base.__init__(self, taintID)

    def Print(self, next, edges):
        print "{} [fillcolor=yellow2 style=filled label=\"{{{{{}}} | {{<size>size = {} | t{} }}}}\"];" \
            .format(self.Label(), self._bytes(), self.size, self.taintID)


class N(Base):
    def __init__(self, size, taintID):
        Base.__init__(self, taintID)
        self.size = size

    def Print(self, next, edges):
        print "{} [fillcolor=green style=filled label=\"{{{{{}}} | {{<size>size = {} | t{} }}}}\"];" \
            .format(self.Label(), self._bytes(), self.size, self.taintID)


class D(Base):
    def __init__(self, size, taintID):
        Base.__init__(self, taintID)
        self.size = size

    def getByte(self, byte):
        if byte in self.byte_sources:
            return self.byte_sources[byte]
        else:
            return self[byte]

    def Print(self, next, edges):
        print "{} [fillcolor=orange style=filled label=\"{{{{{}}} | {{<size>size = {} | t{} }}}}\"];" \
            .format(self.Label(), self._bytes(), self.size, self.taintID)


class M(Base):
    def __init__(self, size, isObject, taintID, *size_deps):
        Base.__init__(self, taintID)
        self.size = size
        self.isObject = isObject
        self.size_deps = size_deps

    def Print(self, next, edges):
        if(self.isObject):
            print "{} [fillcolor=darkgoldenrod style=filled label=\"{{{{{}}} | {{<size>size = {} | t{} }}}}\"];" \
                .format(self.Label(), self._bytes(), self.size, self.taintID)
        else:
            print "{} [fillcolor=darkorchid2 style=filled label=\"{{{{{}}} | {{<size>size = {} | t{} }}}}\"];" \
                .format(self.Label(), self._bytes(), self.size, self.taintID)

        for dep in self.size_deps:
            next.add(dep)
            edges.add("{}:size -> {} [ label=\"t{}\" ];".format(self.Label(), dep.Label(), self.taintID))


def PrintBlocks():
    if args.PRINT_METADATA:
        # print(pointerList)
        print "PointerSet: {}". format(pointerSet)
        print "NameSet: {}".format(nameSet)
        print "AbstractSet: {}".format(abstractDataSet)
        print "ValueSet: {}".format(valueSet)
        sys.exit(0)

    print "digraph {"
    print "node [shape=record];"
    seen, nodes, edges = set(), set(), set()

    # Initialize blocks to be a dictionary of lists.
    # Organize blocks based on their block number.
    blocks = collections.defaultdict(list)
    for b in B.BLOCKS:
        blocks[b.nr].append(b)

    for nr, bs in blocks.items():
        # nr = block number (the key of the dictionary)
        # bs = list of blocks

        if 1 < len(bs):
            # By denoting subgraph as a cluster, the entire drawing of the
            # cluster will be contained within a bounding rectangle.
            print "subgraph cluster{} {{".format(nr)
            print "rankdir=TB;" # Graph will be laid out from top to bottom.

        for b in bs:
            seen.add(b) # Mark block as "seen".
            b.Print(nodes, edges)
            b.PrintByteSources(nodes, edges)
        if 1 < len(bs):
            print "}"

    while nodes:
        node = nodes.pop()
        if node not in seen:
            seen.add(node) # Mark block as "seen" in order not to process it.
            node.Print(nodes, edges)
            node.PrintByteSources(nodes, edges)

    for edge in edges:
        print edge

    print "}"

t0 = NT(0)
