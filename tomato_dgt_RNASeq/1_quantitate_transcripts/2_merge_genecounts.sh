#!/usr/bin/bash

#This script merges (one after the other, not into a matrix) the the gene-level abundance estimates for replicates of the same tissue and genotype

inputpath_genecounts='rsem_genecounts'

if ! [ -d "merged_replicate_counts" ]; then 
	mkdir merged_replicate_counts
fi

#Merge gene counts before calling finding_expressed_genes.py
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/dgt-D[1-3].genes.results > merged_replicate_counts/dgt_D_all.txt
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/dgt-E[1-3].genes.results > merged_replicate_counts/dgt_E_all.txt
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/dgt-M[1-3].genes.results > merged_replicate_counts/dgt_M_all.txt
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/AC-D[1-3].genes.results > merged_replicate_counts/AC_D_all.txt
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/AC-E[1-3].genes.results > merged_replicate_counts/AC_E_all.txt
awk 'NR == 1 || FNR > 1' $inputpath_genecounts/AC-M[1-3].genes.results > merged_replicate_counts/AC_M_all.txt
