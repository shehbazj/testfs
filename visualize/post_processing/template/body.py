# main()
t1=V(0, 1) # Taint<1, 0, 0>
# parse_arguments()
t2=V(1, 2) # Taint<2, 0, 0>
# testfs_init_super_block()
t4=V(64, 4) # Taint<4, 0, 0>
# read_blocks()
t8=A("add",t1,t1, 8)
t9=B(64,0,t4,t8, 9) # GetBlock(64, 0)
t10=A("add",t1,t2, 10)
# read_blocks()
t41=A("add",t10,t2, 41)
t44=O(t9,44,t9[8],t9[9],t9[10],t9[11]) # Load(10633432, 4)
# read_blocks()
t52=A("add",t44,t41, 52)
t53=B(64,6,t4,t52, 53) # GetBlock(64, 6)
