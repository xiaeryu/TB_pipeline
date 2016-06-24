################################################################
## Variant calling and consensus building
################################################################

# input1: input sequence read file 1
# input2: input sequence read file 2 (can be absent for single-end read)
# prefix: prefix of all output files
# reference: reference genome (can use NC_000962.3)
# minR: the minimum read depth for variant calling and consensus building. (can use (0.1 * (#bases after trimming)/ 4500000))


## Index reference sequence. Once for each reference
# name: change the .fasta/.fas of reference to .dict
bwa index $reference
samtools faidx $reference
java -Xmx2g -jar /path/to/picardtools/CreateSequenceDictionary.jar R=$reference O=$name


# Trim adaptors and very low quality reads
java -jar /path/to/trimmomatic/trimmomatic-0.32.jar PE -phred33 -threads 5 \
        $input1 $input2 \
        $prefix-trimmed_R1.fastq.gz $prefix-unpaired_R1.fastq.gz \
        $prefix-trimmed_R2.fastq.gz $prefix-unpaired_R2.fastq.gz \
        ILLUMINACLIP:/path/to/adapters/adapter.fasta:2:30:10 \
        LEADING:3 TRAILING:3

# Alignment and format conversion
bwa mem -R "@RG\tID:$prefix\tSM:$prefix\tLB:$prefix\tPL:Illumina" $reference $prefix-trimmed_R1.fastq.gz $prefix-trimmed_R2.fastq.gz > $prefix.sam
samtools view -bS $prefix.sam -o $prefix.bam

# Sort reads
samtools sort $prefix.bam $prefix.sort
samtools index $prefix.sort.bam

# Indel realn
java -Xmx4g -jar /path/to/GATK/GenomeAnalysisTK.jar -R $reference -T RealignerTargetCreator -o $prefix.realn.intervals -I $prefix.sort.bam
java -Xmx4g -jar /path/to/GATK/GenomeAnalysisTK.jar -R $reference -T IndelRealigner -targetIntervals $prefix.realn.intervals -o $prefix.realn.bam -I $prefix.sort.bam

# Variant calling
samtools mpileup -Q 20 -d 2000 -C 50 -ugf $reference $prefix.realn.bam | /path/to/samtools/bcftools/bcftools view -vcg - > $prefix.vcf

# Filter variant
python filterVCF.py $prefix.vcf > $prefix.filt.vcf

# Calculate read depth
samtools depth $prefix.realn.bam > $prefix.depth

# Build consensus
python buildConsensus.py $reference $prefix.depth $prefix.filt.vcf $minR $prefix > $prefix.consensus.fasta
