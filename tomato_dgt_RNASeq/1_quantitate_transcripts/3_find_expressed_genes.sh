#!/usr/bin/bash

#This script will call finding_expressed_genes.py to pull genes with a TPM above the user defined cutoff
#i.e, will pull genes with an average (between replicates) TPM > min_tpm 

#User defines the cutoffs for TPM and inputpath_genecounts
########################
min_tpm='2' 
inputpath_genecounts='merged_replicate_counts'
########################

if ! [ -d "expressed_genelists" ]; then 
	mkdir expressed_genelists
fi

input_files=`ls $inputpath_genecounts`
for filename in $input_files
do
    file_location=$inputpath_genecounts/$filename
    ./finding_expressed_genes.py $min_tpm $filename $file_location expressed_genelists
done

