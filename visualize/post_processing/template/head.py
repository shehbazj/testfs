import itertools
import sys

labelId = 0

def num_to_taint_object(str):
	return getattr(sys.modules[__name__], str)


def V( a, b):
	return a;

def operate(op, op1, op2):
	if op is "add":
		return op1 + op2
	if op is "mul":
		return op1 * op2
	if op is "sdiv":
		return op1 / op2

def A( op, op1, op2, discard):
	global labelId
	if isinstance(op1,int) and isinstance(op2,int):
		return operate(op, op1, op2)

	elif isinstance(op1,basestring) and isinstance(op2,int):
		if op2 == 0:
			return op1
		labelId+=1
		label = "L"+str(labelId)
		print label,op,op1,op2
		return label

	elif isinstance(op1,list) and isinstance(op2, int):
		mylist = []
		mylist.append(op)
		mylist.append('B')
		mylist.append(op1[-1])  
		mylist.append(op1[0])
		mylist.append(op1[-2])
		mylist.append(op2)
		labelId+=1
		label = "L" + str(labelId)
		print label,mylist
		return label
	else:
		print "No case matched"
		return []

# returns list containing all indexes block number and block taint

def B( bsize, bnum, bsizeTaint, bnumTaint, discard):
	#print 'B [',str(bnum),']'
	mylist = []
	for i in range(0,bsize):
		mylist.append(i)
	mylist.append(bnum)
	#print mylist
	print "B"+str(bnum),bnumTaint
	return mylist

# returns list of indexes and block number

def O(*arg):
	mylist = []
	for name in range(2,len(arg)):
		mylist.append(arg[name])
	mylist.append((arg[0])[-1])	# append block number
	return mylist

if __name__ == "__main__":
    """ Main Start """

