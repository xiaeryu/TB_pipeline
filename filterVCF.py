import sys
import os

if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + " <vcf><min read>"
    sys.exit()

vcf = sys.argv[1]
minR = int(sys.argv[2])

vcfH = open(vcf)
for line in vcfH:
    line = line.strip('\n')
    if not line.startswith('#'):
        tmp = line.split()

        if not tmp[7].startswith('INDEL'):
            info = tmp[7].split(';')
            storage = {}
            for item in info:
                here = item.split('=')
                storage[here[0]] = here[1]

            depth = int(storage['DP'])
            count = storage['DP4'].split(',')
            refCount = int(count[0]) + int(count[1])
            altCount = int(count[2]) + int(count[3])

            filt = []

            if depth >=minR and (refCount+altCount)!=0:
                maf = altCount * 1.0 / (altCount + refCount)
                alt = tmp[4].split(',')
                if maf >= 0.75 and len(alt)==1:
                    filt.append('PASS')

                if len(alt) > 1:
                    filt.append('Fail:MultipleAlt')

                if maf < 0.75:
                    filt.append('Fail:Mix')
            else:
               filt.append('Fail:Depth')

            tmp[6] = ";".join(filt)
            print "\t".join(tmp)

    else:
        print line
vcfH.close()
