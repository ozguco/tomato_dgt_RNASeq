#!/usr/bin/bash

#This script will call finding_upreg_downreg.py and will pull a set of upregulated and downregulated 
#gene lists using the user-defined cutoffs below
#will filter for all genes with postFC > min_upreg_postFC to find upregulated genes 
#will filter for all genes with postFC < max_downreg_postFC to find downregulated genes 
#will filter for all genes with PPDE = PPDE to be considered differentially expressed (either upregulated or downregulated)

#DEFINE CUTOFFS FOR POSTFC AND PPDE HERE
#####################
min_upreg_postFC='2'
max_downreg_postFC='0.5'
desired_PPDE='1'
#####################
ebseq_files='ebseq_diffanalysis_output'

if ! [ -d "upreg_downreg_genelists" ]; then 
	mkdir upreg_downreg_genelists
fi

input_files=`ls $ebseq_files | grep -v .normalized_data_matrix`
for filename in $input_files 
do 
    file_location=$ebseq_files/$filename
    ./finding_upreg_downreg.py $min_upreg_postFC $max_downreg_postFC $desired_PPDE upreg_downreg_genelists $filename $file_location
done 