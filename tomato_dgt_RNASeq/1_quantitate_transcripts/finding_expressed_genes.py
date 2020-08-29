#!/usr/bin/env python

#This program will cycle through each merged RSEM output file and identify expressed genes. 
#User can set cutoffs for the TPM at which a gene is considered "expressed". 

import sys
import pandas as pd 
import numpy as np
import os 

min_tpm = float(sys.argv[1]) 
filename = sys.argv[2]
filepath = sys.argv[3]
output_directory = sys.argv[4]
    
ExpressedGene_filename = str(filename.rsplit(".", 1)[0]) + "_TPMgreater_" + str(min_tpm) + ".txt"
ExpressedGene_file= open(os.path.join(output_directory, ExpressedGene_filename), "w")
    
dataframe = pd.read_csv(filepath, skiprows = 1, sep ="	", names = ["gene_id", "transcript_id(s)", "length", "effective_length", "expected_count", "TPM", "FKPM"])
dataframe.astype({"TPM":float})
average_tpm_df = dataframe.groupby('gene_id')['TPM'].agg('mean').to_frame().reset_index()
average_tpm_df.query('TPM > @min_tpm').to_csv(ExpressedGene_file, sep ="	", index = False)
   
ExpressedGene_file.close()

