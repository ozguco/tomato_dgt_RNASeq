#!/usr/bin/bash

#This will perform the EBSeq analysis
#All gene outputs are dgt upreg/downreg, relative to WT  

call_ebseq=#User insert path to rsem-run-ebseq here
input_datamatrix_location='data_matrix_files'

if ! [ -d "ebseq_diffanalysis_output" ]; then 
	mkdir ebseq_diffanalysis_output
fi 

input_datamatrices=`ls $input_datamatrix_location`

for datamatrix in $input_datamatrices
do 
    zone=`echo $datamatrix | cut -d '_' -f 1` 
    output_file=`echo ${zone}'_diff_expr_genes.txt'`
    $call_ebseq $input_datamatrix_location/$datamatrix 3,3 ebseq_diffanalysis_output/$output_file
done 
