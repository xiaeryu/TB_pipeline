import sys
import os

if len(sys.argv) != 6:
    print "Usage: " + sys.argv[0] + " <reference.fasta><.depth><filt.vcf><min depth><header of consensus>"
    sys.exit()

## Input check
if not os.path.isfile(sys.argv[1]):
    print "ERROR: Invalid reference.fasta!"
    sys.exit()
ref = sys.argv[1]

if not os.path.isfile(sys.argv[2]):
    print "ERROR: Invalid depth file!"
    sys.exit()
depth = sys.argv[2]

if not os.path.isfile(sys.argv[3]):
    print "ERROR: Invalid filt.vcf file!"
    sys.exit()
vcf = sys.argv[3]

minD = int(sys.argv[4])
header = sys.argv[5]

## Code starts here
# Read reference
seq = []
inH = open(ref)
for line in inH:
    if not line.startswith('>'):
        line = line.strip('\n')
        seq.append(line)
inH.close()
seq = "".join(seq)


# Construct the consensus to be N of the same length as the reference
consensus = ["N" for i in xrange(len(seq))]

# Read depth file and set high coverage base to the reference allele
inH = open(depth)
for line in inH:
    line = line.strip('\n')
    tmp = line.split()
    tmp[1] = int(tmp[1])
    tmp[2] = int(tmp[2])
    if tmp[2] >= minD:
        consensus[tmp[1]-1] = seq[tmp[1]-1]
inH.close()

# Read vcf file and include calls
inH = open(vcf)
for line in inH:
    if not line.startswith('#'):
        line = line.strip('\n')
        tmp = line.split()
        tmp[1] = int(tmp[1])

        if tmp[6] == 'PASS':
            consensus[tmp[1]-1] = tmp[4]
        elif tmp[6].startswith('Fail'):
            consensus[tmp[1]-1] = 'N'
inH.close()

## Print
print ">%s" % header
print "".join(consensus)
