#!replace_accession.py
import sys

chrDict = {}

for line in sys.stdin:
    array = line.split("\t")
    ls = [array[0], array[4], array[6], array[9].strip()]
    for index in range(0,len(ls)):
        chrDict[ls[index]] = ls     

col = int(sys.argv[1])

rep = 0 if len(sys.argv) < 4 else int(sys.argv[3])

for line in open(sys.argv[2]):
    if(line.startswith("#") or line.startswith("@")):
        print line
    else:
        array = line.split("\t")
        array[col] = chrDict[array[col]][rep]
        print "\t".join(array)
