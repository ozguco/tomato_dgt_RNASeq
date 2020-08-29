#!/usr/bin/bash

##User inputs locations of the following items##
#processed_genome_annotation should not exist yet. Choose a location and name for this item to be built. 

#######################
genome_sequence=#specify the path to the reference genome sequence file
raw_genome_annotation=#specify the path to the reference genome annotation file
processed_genome_annotation=#specify the location and name for this item to be built 
tomato_fastq_directory=#specify the path to the folder containing fastq files with RNA-Seq reads

call_rsem_prepare_reference=#specify path to rsem-prepare-reference
call_rsem_calculate_expression=#specify path to rsem-calculate-expression
#######################

#Making new directories to place genecount and genome reference files into (unless directory already exists)
if ! [ -d "rsem_genecounts" ]; then 
	mkdir rsem_genecounts
fi 

if ! [ -d "rsem_genomereference" ]; then
	mkdir rsem_genomereference 
fi

#Removes blank lines -- if running RSEM multiple times, comment out the following line 
grep -v 'gene_id ""' $raw_genome_annotation > $processed_genome_annotation

#RSEM prepares the tomato reference genome to align to, using an annotation file and genome sequence file
#if running RSEM multiple times, comment out the following line 
$call_rsem_prepare_reference --gtf $processed_genome_annotation --bowtie $genome_sequence rsem_genomereference/

#then, RSEM will calculate expression using the reference prepared above and the RNA-seq data files
#user can change the output_filename variable to reflect their desired naming convention

rnaseq_filelist=`ls $tomato_fastq_directory |grep -e Sample_lane1 -e Sample_lane2`

for rnaseq_file in $rnaseq_filelist
do 
    output_filename=`echo $rnaseq_file| cut -d '.' -f 1 | cut -d '-' -f 4,5`
    $call_rsem_calculate_expression -p 20 $tomato_fastq_directory/$rnaseq_file rsem_genomereference/ rsem_genecounts/$output_filename
done 

