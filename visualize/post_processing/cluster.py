import sys
import shutil
import os

nextFile = 0
allFiles = []

def commonCksum(f1,f2):
	cksum1 = set(open(f1,'r'))
	cksum2 = set(open(f2,'r'))
	if cksum1.isdisjoint(cksum2):
		return False
	return True

def getNextFile():
	global nextFile
	global allFiles
	if nextFile > (len(allFiles)-1):
		#print "returning none since nextFile = ",nextFile,"len of allFiles = ",len(allFiles)
		return None
	else:
		#print "returning ",nextFile,allFiles[nextFile]
		return allFiles[nextFile]	
	
if __name__ == "__main__":
    """ Main Start """
allFiles=sys.argv[1:len(sys.argv)]
#print allFiles

f1=getNextFile()
nextFile+=1
#print "f1 returned",f1
while f1:
	f2=getNextFile()
	#print "f2 returned",f2
	if f2 is None:
		break
	if commonCksum(f1,f2) == True:
		#print f1,f2,"Match"
		f=f1+'.'+f2
		#print "name of f",f," after merging ",f1,f2
		mergeFile=open(f, "w")
		fileOne=open(f1,"r")
		fileTwo=open(f2,"r")
		mergeFile.write(fileOne.read())
		mergeFile.write(fileTwo.read())
		mergeFile.close()
		fileOne.close()
		fileTwo.close()
		os.remove(f1)
		os.remove(f2)
		allFiles.remove(f1)
		allFiles.remove(f2)
		allFiles.insert(0,f)		
		#print "all Files = ",allFiles
		f1=f
	else:
		nextFile+=1
		#print f1,f2,"No Match"
		f1=f2

#print allFiles
#print commonCksum(f1,f2)
