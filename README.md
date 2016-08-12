TB Analysis pipeline
===

Sequencing reads
---
* **Quality inspection** [fastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* **Variant calling** [Pipeline](https://github.com/xiaeryu/TB_pipeline/blob/master/VariantCalling.sh)
* **Consensus building** [Pipeline](https://github.com/xiaeryu/TB_pipeline/blob/master/VariantCalling.sh)
* **Strain typing using [SNP barcoding](http://www.nature.com/articles/ncomms5812)** [62 SNP markers](https://github.com/xiaeryu/TB_pipeline/blob/master/Scheme_62) & [Script](https://github.com/xiaeryu/TB_pipeline/blob/master/Barcoding.py)
* **Spoligotyping** [SpoTyping](https://github.com/xiaeryu/SpoTyping/releases/) or [SpolPred](http://pathogenseq.lshtm.ac.uk/spolpred)
* **RD analysis** [RD-Analyzer](https://github.com/xiaeryu/RD-Analyzer)

Genome assemblies
---
* **Variant calling using [MUMmer](http://mummer.sourceforge.net/)** [Command](https://github.com/xiaeryu/TB_pipeline/blob/master/VariantCalling_assembly.sh)
* **Strain typing using [SNP barcoding](http://www.nature.com/articles/ncomms5812)** [62 SNP markers](https://github.com/xiaeryu/TB_pipeline/blob/master/Scheme_62) & [Script](https://github.com/xiaeryu/TB_pipeline/blob/master/Barcoding_assembly.py)
* **Spoligotyping** [SpoTyping](https://github.com/xiaeryu/SpoTyping/releases/)
* **RD analysis** [RD-Analyzer for sequence](https://github.com/xiaeryu/TB_pipeline/blob/master/RD-Analyzer_assembly.py) [RDs](https://github.com/xiaeryu/RD-Analyzer/blob/master/RD-Analyzer.py)
