#!/usr/bin/bash

#This script takes a set of rsem .genes.results output files and generates a matrix that can then be used for EbSeq 

#The way this script is currently set up places dgt as condition 1 and WT as condition 2. This will result in an analysis along the lines of 
#"dgt upregulated/downregulated relative to WT". If you want the opposite (WT relative to dgt), AC files will need to be 
#added to the matrix first (i.e, place $input_genecounts/AC-D[1-3].genes.results in front of $input_genecounts/dgt-D[1-3].genes.results instead of 
#behind in the lines below)

input_genecounts='../1_quantitate_transcripts/rsem_genecounts'
call_rsemdatamatrix=#User insert path to rsem-generate-data-matrix here

if ! [ -d "data_matrix_files" ]; then 
	mkdir data_matrix_files
fi 

$call_rsemdatamatrix $input_genecounts/dgt-D[1-3].genes.results $input_genecounts/AC-D[1-3].genes.results > data_matrix_files/D_gene_counts.txt
$call_rsemdatamatrix $input_genecounts/dgt-E[1-3].genes.results $input_genecounts/AC-E[1-3].genes.results > data_matrix_files/E_gene_counts.txt
$call_rsemdatamatrix $input_genecounts/dgt-M[1-3].genes.results $input_genecounts/AC-M[1-3].genes.results > data_matrix_files/M_gene_counts.txt

