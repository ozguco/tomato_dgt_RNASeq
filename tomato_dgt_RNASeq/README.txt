TITLE: RNA-Seq analysis of genes affected by Cyclophilin A/DIAGEOTROPICA (DGT) in tomato root development
LAST UPDATED: Aug-29-2020
LAST UPDATED BY: OZGUC, O.

Cyclophilin A/DIAGEOTROPICA (DGT) has been linked to auxin-regulated development in tomato and appears to affect 
multiple developmental pathways. Loss of DGT function results in a pleiotropic phenotype that is strongest in the 
roots, including shortened roots with no lateral branching. Here, we present the pipeline for analyzing an RNA-Seq 
dataset comparing the gene expression profiles of wildtype (‘Ailsa Craig’) and dgt tissues from three spatially  
separated developmental stages of the tomato root tip, with three replicates for each tissue and genotype. 

This pipeline uses RSEM (version 1.3.1) and EBSeq (version 1.26.0) to perform presence/abscence calls and identify 
differentially expressed genes. The user can set TPM cutoffs for presence/abscence calls and postFC/PPDE cutoffs 
for differential expression analysis. Also provided are the scripts for generating figures as seen in the associated
manuscript. 
------------------------------------------------------------------------------------------------------------------

            #############################################################
            #                      REQUIREMENTS                         #
            #############################################################
                        
SOFTWARE
- RSEM (version 1.3.1), available from https://github.com/deweylab/RSEM/releases/tag/v1.3.1
- EBSeq (version 1.26.0), available from https://bioconductor.org/packages/3.11/bioc/html/EBSeq.html 
- Python (3.0 or later) and the following packages: 
    - sys 
    - os 
    - pandas 
    - numpy 
    - matplotlib 
    - matplotlib_venn
    - scikit-learn

DATA
- Heinz 1706 reference genome and annotation (or reference genome of choice), available from
  ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/188/115/GCF_000188115.4_SL3.0  
- Raw RNA-Seq reads (demultiplexed), available from NCBI Sequence Read Archive as described in manuscript.

            #############################################################
            #                     PIPELINE OVERVIEW                     #
            #############################################################

STEP-A  QUANTITATE TRANSCRIPTS

    1: prepare reference genome/annotation using rsem-prepare-reference
    2: align reads to reference and estimate abundance using rsem-calculate-expression 
    Steps accomplished by: 1_quantitate_transcripts/1_run_rsem.sh

STEP-B  PRESCENCE/ABSCENCE CALLS

    1: merge replicates and filter genes based on TPM
    Steps accomplished by: 1_quantitate_transcripts/2_merge_genecounts.sh and 
    1_quantitate_transcripts/3_find_expressed_genes.sh
      
STEP-C  FIND DIFFERENTIALLY EXPRESSED GENES 

    1: run EBSeq on RSEM abundance estimate output using rsem-run-ebseq
    2: filter genes based on PPDE and postFC
    Steps accomplished by: 2_differential_gene_expression/1_prep_datamatrix.sh, 
    2_differential_gene_expression/2_run_ebseq.sh, and 2_differential_gene_expression/3_find_upreg_downreg.sh


            #############################################################
            #                     DETAILED INSTRUCTIONS                 #
            #############################################################

A. GENERATE EXPRESSION ESTIMATES USING RSEM
Navigate to 1_quantitate_transcripts
In 1_quantitate_transcripts/: 
    1. Edit 1_run_rsem.sh with the locations of your reference genome sequence, reference genome annotation, fastq 
    files, desired location for a processed genome annotation file (this will be built), and RSEM location. 
        For example, a user who had their reference genome sequence and annotation in a directory titled 
        'input_data_repository',fastq files in a sub-directory titled 'raw_fastq', and RSEM in a directory titled 
        'software' might enter: 
            genome_sequence='.../input_data_repository/GCF_000188115.4_SL3.0_genomic.fna'
            raw_genome_annotation='.../input_data_repository/GCF_000188115.4_SL3.0_annotation.gtf'
            processed_genome_annotation='.../input_data_repository/GCF_000188115.4_SL3.0_annotation_noblanks.gtf'
            raw_fastq='.../input_data_repository/raw_fastq'
            call_rsem_prepare_reference='../software/RSEM/RSEM-1.3.1/rsem-prepare-reference'
            call_rsem_calculate_expression='../software/RSEM/RSEM-1.3.1/rsem-calculate-expression'
    2. Run 1_run_rsem.sh (./1_run_rsem.sh)
        Note: if you are running RSEM multiple times or have already used rsem-prepare-reference to prepare your 
        reference, comment out the lines for generating a reference in the script. 

B. PRESENCE/ABSCENCE CALLS -- AFTER A. IS COMPLETE
In 1_quantitate_transcripts/: 
    1. Run 2_merge_genecounts.sh (./2_merge_genecounts.sh) to merge .genes.results files for replicates of same 
       tissue/genotype. 
    2. After 2_merge_genecounts.sh completes, run 3_find_expressed_genes.sh (./3_find_expressed_genes.sh) to filter
       for genes with an average TPM greater than a user-defined cutoff. 
       Note: If you want to edit TPM cutoff, do so by editing the min_tpm variable in 3_find_expressed_genes.sh

C. DIFFERENTIAL EXPRESSION -- AFTER A. IS COMPLETE
Navigate to 2_differential_gene_expression
In 2_differential_gene_expression/: 
    1. Edit 1_prep_datamatrix.sh with path to rsem-generate-data-matrix software and 2_run_ebseq.sh with path to 
    rsem-run-ebseq. 
        For example, a user who had RSEM in a directory titled 'software' might enter: 
        call_rsemdatamatrix='../software/RSEM/RSEM-1.3.1/rsem-generate-data-matrix'
        and 
        call ebseq='../software/RSEM/RSEM-1.3.1/rsem-run-ebseq'
    2. Run 1_prep_datamatrix.sh to generate a matrix of all counts for samples of the same tissue type. 
    3. After 1_prep_datamatrix.sh completes, run 2_run_ebseq.sh to generate postFC and PPDE values for each gene. 
    4. After 2_run_ebseq.sh completes, run 3_find_upreg_downreg.sh to filter for genes over/under a set postFC
       value and equal to a set PPDE value. 
       Note: if you want to edit PPDE/postFC cutoffs, do so by editing the min_upreg_postFC, max_downreg_postFC, 
       and desired_PPDE variables 

            #############################################################
            #                       ADDITIONAL TOOLS                    #
            #############################################################

The 3_analysis/ subfolder contains tools for further analyzing and displaying results, and can be used in part or in whole 
as desired. Within this subfolder are scripts used to generate venn diagrams and perform principal component analysis.
Each script has a usage statement that will be displayed to the user if run without the required command line inputs. 

In brief, the scripts below require the following inputs and accomplish the following goals: 
    - venn_diagrams_figure1AB.py: generates 3-circle venn diagram comparing expressed genes between tissue types from a 
      given genotype
            * Input: D, E, and M gene lists (select either files beginning with 'AC' or 'dgt') generated from 
            1_quantitate_transcripts/3_find_expressed_genes.sh and placed in 1_quantitate_transcripts/expressed_genelists
    - venn_diagrams_figure1CDE.py: generates 2-circle venn diagram comparing expressed genes that were present in only 
      one tissue type between WT and dgt. 
            * Input: D_only, E_only, and M_only gene lists (select either "D", "E", or "M" to analyze and use the sets from
            both WT and dgt) generated by venn_diagrams_figure1AB.py and placed in 3_analysis/gene_lists
            NOTE: venn_diagrams_figure1CDE.py must be run *after* venn_diagrams_figure1AB.py as this script uses output gene 
            lists from venn_diagrams_figure1AB.py.
    - venn_diagrams_figure2.py: generates 3-circle venn diagram comparing differentially expressed genes between WT and dgt.
            * Input: lists of upregulated or downregulated genes from each developmental zone, generated by 
              2_differential_gene_expression/3_find_upreg_downreg.sh and placed in 2_differential_gene_expression/upreg_downreg_genelists. 
    - PCA_biplot.py: performs principal component analysis to compare TPM values from .genes.results files between replicates 
      of dgt and WT samples in different developmental zones
            * Input: .genes.results files for all samples from a given developmental zone, generated by 
              1_quantitate_transcripts/1_run_rsem.sh and placed in 1_quantitate_transcripts/rsem_genecounts


