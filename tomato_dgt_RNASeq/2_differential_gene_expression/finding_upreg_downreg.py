#!/usr/bin/env python

#This program will cycle through each of the EBSeq output file and identify upregulated/downregulated genes.  
#If a value is empty for PPDE or PostFC, the gene will not be included in analysis. 

import sys 
import pandas as pd 
import numpy as np 
import os 

min_upreg_postFC = float(sys.argv[1])
max_downreg_postFC = float(sys.argv[2])
desired_PPDE = float(sys.argv[3])
output_directory = sys.argv[4]
filename = sys.argv[5]
filepath = sys.argv[6]
	
upregfile_name = str(filename.rsplit(".", 1)[0]) + "_PPDE" + str(desired_PPDE) + "_postFCgreater"+str(min_upreg_postFC)+".txt"
downregfile_name = str(filename.rsplit(".", 1)[0]) + "_PPDE" + str(desired_PPDE) + "_postFCless"+str(max_downreg_postFC)+".txt"
upregfile = open(os.path.join(output_directory, upregfile_name), "w") 
downregfile = open(os.path.join(output_directory, downregfile_name), "w")

dataframe = pd.read_csv(filepath, skiprows = 1, sep="	", names = ["gene_id", "PPEE", "PPDE", "POSTFC", "REALFC", "C1_mean", "C2_mean"])
dataframe.astype({"PPDE": float, "POSTFC" : float})
#In the following two lines, the parameters can be modified (for example, if you'd like to look at realFC instead of postFC. 
dataframe.query('PPDE == @desired_PPDE and POSTFC > @min_upreg_postFC').to_csv(upregfile, sep = "	", index = False)
dataframe.query('PPDE == @desired_PPDE and POSTFC < @max_downreg_postFC').to_csv(downregfile, sep = "	", index = False)

upregfile.close()
downregfile.close()