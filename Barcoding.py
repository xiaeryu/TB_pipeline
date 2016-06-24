import sys
import os

if len(sys.argv) != 3:
    print "Usage: " + sys.argv[0] + " <Scheme file><.filt.vcf>"
    sys.exit()

## Guard
if not os.path.isfile(sys.argv[1]):
    print "ERROR: Invalid scheme file!"
    sys.exit()
scheme = sys.argv[1]

if not os.path.isfile(sys.argv[2]):
    print "ERROR: Invalid .filt.vcf file!"
    sys.exit()
vcf = sys.argv[2]

##Read vcf
##Each line in vcf:
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  $prefix
variant = {}
inH = open(vcf)
for line in inH:
    if not line.startswith('#'):
        line = line.strip('\n')
        tmp = line.split()
#        if tmp[6] == 'PASS':
        if True:
            variant[tmp[1]] = tmp[4].upper()
inH.close()

##Read scheme
##Each line in scheme:
#lineage1        615938  1104    G/A     368     GAG/GAA         E/E     Rv0524  hemL
strain = []

inH = open(scheme)
for line in inH:
    if not line.startswith('#'):
        line = line.strip('\n')
        tmp = line.split()
        lineage = tmp[0]
        pos = str(tmp[1])
        alt = (tmp[3].split('/'))[1]
        if pos in variant and variant[pos] == alt.upper():
            strain.append(lineage+"/"+pos)

inH.close()


print vcf + "\t" + "\t".join(strain)
