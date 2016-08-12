## Using nucmer and show-snps in MUMmer

nucmer --maxmatch -c 100 -p $prefix reference.fasta input.fasta; show-snps -CIlr $prefix.delta > $prefix.snp
