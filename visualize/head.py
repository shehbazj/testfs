import collections

class Base(object):
  def __init__(self):
    self.size = 1
    self.byte_sources = {}

  def __getitem__(self, byte):
    self.size = max(self.size, byte + 1)
    return Select(self, byte)

  def __setitem__(self, byte, val):
    self.byte_sources[byte] = val

  def Label(self):
    return "n{}".format(id(self))

  def PrintByteSources(self, next, edges):	# add all values from byte_sources
    for i, s in self.byte_sources.items():	# list to next list
      next.add(s)
      edges.add("{}:b{} -> {};".format(self.Label(), i, s.Label())) # set n

  def _bytes(self):
    return "|".join("<b{}>".format(i) for i in range(self.size))


class Select(Base):
  def __init__(self, parent, byte):
    Base.__init__(self)
    self.parent = parent
    self.byte = byte

  def Print(self, next, edges):
    next.add(self.parent)

  def Label(self):
    return "{}:b{}".format(self.parent.Label(), self.byte)


class V(Base):
  def __init__(self, val):
    Base.__init__(self)
    self.val = val

  def Print(self, next, edges):
    print "{} [label=\"{{{{{}}}|{}}}\"];".format(self.Label(), self._bytes(), hex(self.val))


class A(Base):
  def __init__(self, op, a, b):
    Base.__init__(self)
    self.op = op
    self.left = a
    self.right = b

  def Print(self, next, edges):
    if isinstance(self.left, V):
      LL = str(self.left.val)
    else:
      next.add(self.left)
      LL = "<left>"
      edges.add("{}:left -> {};".format(self.Label(), self.left.Label()))

    if isinstance(self.right, V):
      RL = str(self.right.val)
    else:
      next.add(self.right)
      RL = "<right>"
      edges.add("{}:right -> {};".format(self.Label(), self.left.Label()))

    print "{} [color=blue label=\"{{ {{ {} }} |{}| {{{}|{}}} }}\"];".format(
        self.Label(), self._bytes(), self.op, LL, RL)


class O(Base):
  def __init__(self, *bytes):
    Base.__init__(self)
    self.bytes = bytes
    self.size = len(self.bytes)

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
      edges.add("{}:b{} -> {};".format(self.Label(), i, b.Label()))


class B(Base):
  BLOCKS = []

  def __init__(self, size, nr, block_size, block_nr):
    Base.__init__(self)
    self.size = size
    self.nr = nr
    self.block_size = block_size
    self.block_nr = block_nr
    self.BLOCKS.append(self)

  def Print(self, next, edges):
    print "{} [rank=max fillcolor=grey style=filled label=\"{{{{{}}}|{{<size>size = {}|<nr>nr = {} }}}}\"];".format(
        self.Label(), self._bytes(), self.size, self.nr)
    
    if not isinstance(self.block_size, V):
      next.add(self.block_size)
      edges.add("{}:size -> {};".format(self.Label(), self.block_size.Label()))
    
    if not isinstance(self.block_nr, V):
      next.add(self.block_nr)
      edges.add("{}:nr -> {};".format(self.Label(), self.block_nr.Label()))


class N(Base):
  def __init__(self, size):
    Base.__init__(self)
    self.size = size

  def Print(self, next, edges):
    print "{} [fillcolor=green style=filled label=\"{}\"];".format(self.Label(), self._bytes())


class D(Base):
  def __init__(self, size):
    Base.__init__(self)
    self.size = size

  def Print(self, next, edges):
    print "{} [fillcolor=orange style=filled label=\"{}\"];".format(self.Label(), self._bytes())


class M(Base):
  def __init__(self, size, *size_deps):
    Base.__init__(self)
    self.size = size
    self.size_deps = size_deps

  def Print(self, next, edges):
    print "{} [fillcolor=blue style=filled label=\"{}\"];".format(self.Label(), self._bytes())
    #for dep in self.size_deps:
    #  next.add(dep)
    #  edges.add("{}:size -> {}")


def PrintBlocks():
  print "digraph {"
  print "node [shape=record];"
  seen, nodes, edges = set(), set(), set()
    
  blocks = collections.defaultdict(list)
# add all BLOCK variables from B() list into blocks list
# the list is indexed by their block number - b.nr

  for b in B.BLOCKS:
    blocks[b.nr].append(b)
# XXX bs contains the block address. len (bs) gives 1.  
# if bs contains a subgraph structure, we need to draw that
# in either case, we take individual element in bs and process it 

  for nr, bs in blocks.items():
    if 1 < len(bs):
      print "subgraph cluster{} {{".format(nr)
      print "rankdir=TB;"
    for b in bs:
# add the block that has been traversed into the "seen" list
      seen.add(b)
# print the grey boxes. Also, see if "nr" and "size" parameters
# are instances of V. if not, create node element and add it
# to nodes list. create edges element and add edge
      b.Print(nodes, edges)
# PrintByteSources - will not print any new output on
# the xdot file. 
# Assign a node to each byte. add edges from
# byte to the node. At the end, we would have created 64 nodes
# for each byte in the block, with 64 edges, each edge 
# identified by block node id:byte_offset and byte node id
      b.PrintByteSources(nodes, edges)
    if 1 < len(bs):
      print "}"

  while nodes:
    node = nodes.pop()
    if node not in seen:        # these are nodes corresponding to
      seen.add(node)            # size, number and byte for each
      node.Print(nodes, edges)  # block
      node.PrintByteSources(nodes, edges)
  
  for edge in edges:
     print edge

  print "}"

t0 = V(0x0)
