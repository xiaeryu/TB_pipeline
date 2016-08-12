import sys
import os
import subprocess


###################################
# Input options & checks
###################################

if len(sys.argv) < 5:
    print "Usage: " + sys.argv[0] + " <input query fasta file> <reference file> <minimum coverage*identity as a cutoff, 0-100> <output file>"
    sys.exit()

if not os.path.isfile(sys.argv[1]):
    print "Cannot find input query fasta file!"
    sys.exit()
else:
    query = sys.argv[1]

if not os.path.isfile(sys.argv[2]):
    print "Cannot find input reference file!"
    sys.exit()
else:
    reference = sys.argv[2]

output = sys.argv[4]

coverage = float(sys.argv[3])

if coverage <=0 or coverage > 100:
    print "Coverage*identity cutoff should be between 0 and 100."
    sys.exit()


###################################
# Functions
###################################
class Main:
    def predLineage(self, inDict):
        inLineage = {
            "L1":"Mtb: Indo-Oceanic - Lineage 1 - (RD239)",
            "L21":"Mtb: East Asian - Lineage 2.1 - (RD105)",
            "L221":"Mtb: East Asian - Lineage 2.2.1 - (RD105,207,181)",
            "L2211":"Mtb: East Asian - Lineage 2.2.1.1 - (RD105,207,181,150)",
            "L2212":"Mtb: East Asian - Lineage 2.2.1.2 - (RD105,207,181,142)",
            "L222":"Mtb: East Asian - Lineage 2.2.2 - (RD105,207)",
            "L3":"Mtb: East-African-Indian - Lineage 3 - (RD750)",
            "L4111":"Mtb: Euro-American - Lineage 4.1.1.1 - (pks15/1:7D, RD183)",
            "L4113":"Mtb: Euro-American - Lineage 4.1.1.3 - (pks15/1:7D, RD193)",
            "L4121":"Mtb: Euro-American - Lineage 4.1.2.1 - (pks15/1:7D, RD182)",
            "L4321":"Mtb: Euro-American - Lineage 4.3.2.1 - (pks15/1:7D, RD761)",
            "L433":"Mtb: Euro-American - Lineage 4.3.3 - (pks15/1:7D, RD115)",
            "L434":"Mtb: Euro-American - Lineage 4.3.4 & sublineages - (pks15/1:7D, RD174)",
            "L45":"Mtb: Euro-American - Lineage 4.5 - (pks15/1:7D, RD122)",
            "L461":"Mtb: Euro-American - Lineage 4.6.1 & sublineages - (pks15/1:7D, RD724)",
            "L462":"Mtb: Euro-American - Lineage 4.6.2 & sublineages - (pks15/1:7D, RD726)",
            "L4o":"Mtb: Euro-American - Lineage 4.2, 4.4, 4.7 H37Rv-like and others - (pks15/1:7D)",
            "L48":"Mtb: Euro-American - Lineage 4.8 - (pks15/1:7D, RD219)",
            "L5":"M.africanum I - Lineage 5 - (RD9, 711)",
            "L6":"M.africanum II - Lineage 6 - (RD9, 7,8,10, pks15/1:6D, 702)",
            "Mmic":"M.microti - (RD9, 7,8,10, pks15/1:6D, 1mic)",
            "Mpin":"M.pinnipedii - (RD9, 7,8,10, pks15/1:6D, 2seal)",
            "Mcap":"M.caprae - (RD9, 7,8,10, pks15/1:6D, 12bov)",
            "Mbov":"M.bovis (classical) - (RD9, 7,8,10, pks15/1:6D, 12bov, 4)",
            "Mbb1":"M.bovis BCG (Moreau) - (RD9, 7,8,10, pks15/1:6D, 12bov, 4, 1bcg",
            "Mbb2":"M.bovis BCG (Merieux) - (RD9, 7,8,10, pks15/1:6D, 12bov, 4, 1bcg, 2bcg)",
            "Mcan":"M.canettii - (RD12bov, 12can)",
        }

        lineage = []
        if inDict['RD239_15'] == 'A':
            lineage.append("L1")
        if inDict['RD105_14'] == 'A' and inDict["RD142_17"] == 'P' and inDict["RD150_18"] == 'P' and inDict["RD181_19"] == 'P' and inDict["RD207_20"] == 'P':
            lineage.append("L21")
        if inDict['RD105_14'] == 'A' and inDict["RD181_19"] == 'A' and inDict["RD207_20"] == 'A' and inDict["RD142_17"] == 'P' and inDict["RD150_18"] == 'P':
            lineage.append("L221")
        if inDict['RD105_14'] == 'A' and inDict["RD181_19"] == 'A' and inDict["RD207_20"] == 'A' and inDict["RD142_17"] == 'P' and inDict["RD150_18"] == 'A':
            lineage.append("L2211")
        if inDict['RD105_14'] == 'A' and inDict["RD181_19"] == 'A' and inDict["RD207_20"] == 'A' and inDict["RD142_17"] == 'A' and inDict["RD150_18"] == 'P':
            lineage.append("L2212")
        if inDict['RD105_14'] == 'A' and inDict["RD142_17"] == 'P' and inDict["RD150_18"] == 'P' and inDict["RD181_19"] == 'P' and inDict["RD207_20"] == 'A':
            lineage.append("L222")

        if inDict['RD750_16'] == 'A' and inDict["7bp_pks15.1"] == 'Complete':
            lineage.append("L3")

        if inDict["7bp_pks15.1"] == '7D' and inDict["RD183_25"] == 'A':
            lineage.append("L4111")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD193_26"] == 'A':
            lineage.append("L4113")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD182_24"] == 'A':
            lineage.append("L4121")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD761_30"] == 'A':
            lineage.append("L4321")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD115_21"] == 'A':
            lineage.append("L433")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD174_23"] == 'A':
            lineage.append("L434")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD122_22"] == 'A':
            lineage.append("L45")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD724_28"] == 'A':
            lineage.append("L461")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD726_29"] == 'A':
            lineage.append("L462")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD183_25"] == 'P' and inDict["RD193_26"] == 'P' and inDict["RD182_24"] == 'P' and inDict["RD761_30"] == 'P' and inDict["RD115_21"] == 'P' and inDict["RD174_23"] == 'P' and inDict["RD122_22"] == 'P' and inDict["RD724_28"] == 'P' and inDict["RD726_29"] == 'P' and inDict["RD219_27"] == 'P':
            lineage.append("L4o")
        if inDict["7bp_pks15.1"] == '7D' and inDict["RD219_27"] == 'A':
            lineage.append("L48")

        if inDict['RD12can_13'] == 'A' and inDict['RD9_1'] == 'P' and inDict["7bp_pks15.1"] == 'Complete':
            lineage.append("Mcan")
        if inDict['RD711_2']=='A' and inDict['RD1mic_6'] == 'P':
            lineage.append("L5")
        if inDict['RD702_3']=='A' and inDict["7bp_pks15.1"] =='6D':
            lineage.append("L6")
        if inDict['RD1mic_6'] == 'A':
            lineage.append("Mmic")
        if inDict['RD2seal_7'] == 'A' and inDict["7bp_pks15.1"] == '6D' and inDict['RD711_2'] == 'P' and inDict['RD2bcg_8'] == 'P':
            lineage.append("Mpin")
        if inDict['RD12bovis_12'] == 'A' and inDict["7bp_pks15.1"] =='6D' and inDict['RD2bcg_8'] == 'P' and inDict['RD1bcg_5'] == 'P' and inDict['RD4_4'] == 'P':
            lineage.append("Mcap")
        if inDict['RD4_4'] == 'A' and inDict['RD2bcg_8'] == 'P' and inDict['RD1bcg_5'] == 'P':
            lineage.append("Mbov")
        if inDict['RD4_4'] == 'A' and inDict['RD2bcg_8'] == 'P' and inDict['RD1bcg_5'] == 'A':
            lineage.append("Mbb1")
        if inDict['RD4_4'] == 'A' and inDict['RD2bcg_8'] == 'A' and inDict['RD1bcg_5'] == 'A':
            lineage.append("Mbb2")

        if len(lineage) == 0:
            return "Unidentified"

        return '; '.join([inLineage[item] for item in lineage])


###################################
# Record reference information
###################################
storage = {}
trace = ""
inH = open(reference)
for line in inH:
    line = line.strip('\n')
    if line.startswith('>'):
        line = line.lstrip('>')
        trace = line
        if trace != '7bp_pks15.1':
            storage[trace] = [0,0,0,0]
        else:
            storage[trace]= " "
    elif trace != '7bp_pks15.1':
        storage[trace][0] += len(line)
inH.close()


###################################
# BLAST for output
###################################
subprocess.call(["makeblastdb", "-in", reference, "-out", reference, "-dbtype", "nucl"])
subprocess.call(["blastn", "-query", query, "-db", reference, "-task", "blastn", "-outfmt", "6 qseqid qlen sseqid qstart qend sstart send length pident bitscore qseq sseq", "-out", query + "_blast.out"])

###################################
# Parse blast output
###################################
RDs = ["RD9_1","RD711_2","RD702_3","RD4_4","RD1bcg_5","RD1mic_6","RD2seal_7","RD2bcg_8","RD7_9","RD8_10","RD10_11","RD12bovis_12","RD12can_13","RD105_14","RD239_15","RD750_16","RD142_17","RD150_18","RD181_19","RD207_20","RD115_21","RD122_22","RD174_23","RD182_24","RD183_25","RD193_26","RD219_27","RD724_28","RD726_29","RD761_30"]
resultDict = {}
for RD in RDs:
    resultDict[RD] = 'P'
resultDict["7bp_pks15.1"] = 'Complete'


inH = open(query + "_blast.out")
for line in inH:
    line = line.strip('\n')
    tmp = line.split()

    if tmp[2] != '7bp_pks15.1':
        if float(tmp[9]) > storage[tmp[2]][3]:
            storage[tmp[2]][1] = int(tmp[7])
            storage[tmp[2]][2] = float(tmp[8])
            storage[tmp[2]][3] = float(tmp[9])
    else:
        G7 = tmp[10].find('-------')
        if G7 >= 152 and G7 <= 176:
            storage[tmp[2]] = "7D"
            resultDict[tmp[2]] = "7D"
        else:
            G6 = tmp[10].find('------')
            if G6 >= 152 and G6 <= 176:
                storage[tmp[2]] = "6D"
                resultDict[tmp[2]] = "6D"
            else:
                storage[tmp[2]] = 'Complete'
inH.close()

for item in storage:
    if item != '7bp_pks15.1':
        if storage[item][1] * 1.0 * storage[item][2] / storage[item][0] < coverage:
            resultDict[item] = "A"


###################################
# Predict lineage
###################################
t=Main()
lineage = t.predLineage(resultDict)


outH = open(output, 'w')

outH.write("# Input file: " + query + '\n')
outH.write("# Cutoff: " + str(coverage) + '\n')
outH.write("\n# Predicted lineage: " + lineage + '\n\n')

outH.write("Name\tRef-len\tCov-len\tCoverage\tIdentity\tPrediction\n")

for item in storage:
    if item != '7bp_pks15.1':
        outH.write("%s\t%d\t%d\t%.2f\t%.1f\t%s\n" % (item, storage[item][0], storage[item][1], storage[item][1] * 1.0 / storage[item][0], storage[item][2], resultDict[item]))

item='7bp_pks15.1'
outH.write("%s\t--\t--\t--\t--\t%s\n" % (item, storage[item]))

outH.close()
