#!/usr/bin/env python 

import sys
import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA 
from matplotlib import pyplot as plt

#This script takes either a single dgt and single WT data matrix or six total data files (3x dgt, 3x WT), performs principal component analysis, and generates a plot of PC1 vs PC2 comparing the dgt and WT datasets
#This script has been set up to use the .genes.results files generated in 1_quantitate_transcripts/1_run_rsem.sh
#Repeat for each zone: differentiation zone, elongation zone, and meristem, and change the plot_title variable below to reflect the developmental zone and any other information you would like included in the title


#Usage statement 
#Input must either be a dataframe in which first column is gene_ID, next 3 columns are dgt samples and final 3 columns are WT samples; or, a list of files from which to make such a data frame 
#Order of columns in dataframe MUST be 3 dgt followed by 3 WT. If changing order, 'conditions' dictionary must also be changed. 
usage = "This script takes an input data frame (containing genes as rows and conditions as columns), calculates principal components, and creates biplot using PC1 and PC2. Usage: <single or multiple files? Write either single or multiple><name for output figure (without extension)><input data frame file location or .genes.results files from which to make frame organized with 3 DGT files followed by 3 WT files><output file name>. You will need to edit figure title within script. " 
if len(sys.argv) < 4: 
    print(usage)
    sys.exit()

#User defined variables 
plot_title = "Elongation Zone"     #Change this variable to what you would like plot title to be 

#Functions 
#create_frame function will take all .genes.results files in the user supplied folder and pull the TPM column from each
#If you want to use a different column instead of TPM, change "TPM" in usecols to label of column of interest. 
def create_frame(file_list): 
    header_filenames = [] 
    df = pd.DataFrame()
    for file in file_list: 
        temp_df = pd.read_csv(file, header = 0, sep="	", usecols =["gene_id", "TPM"]).set_index('gene_id')
        df = pd.concat([df, temp_df], axis=1) 
        filename = (file.split(sep="/"))[-1]
        header_filenames.append(filename)
    df.columns = header_filenames
    return df

#Inputs from command line and decision of whether data frame needs to be made or user will supply ready-made data frame

input_type = sys.argv[1]
figname = sys.argv[2]
input_files = sys.argv[3:]
fig_filename = figname + ".png"


#Load or generate data frame 
if input_type == "single": 
    df = pd.read_csv(input_files[0], sep = "	", index_col = 0) 
elif input_type == "multiple": 
    df = (create_frame(input_files))
else:
    print(usage)
    sys.exit()

#Transpose so that gene_IDs are columns and genotypes are rows  
df_transposed = df.T

#Standardize the data 
df_ss = StandardScaler().fit_transform(df_transposed)
pca_model = PCA()
pca_out = pca_model.fit_transform(df_ss)
print(pca_model.explained_variance_ratio_) 
PC1_expvar = round(((pca_model.explained_variance_ratio_)[0])*100, 1)
PC2_expvar = round(((pca_model.explained_variance_ratio_)[1])*100, 1)
print(PC1_expvar)
print(PC2_expvar)

conditions = {'conditions': ['dgt', 'dgt','dgt','WT', 'WT', 'WT']} 
condition_df = pd.DataFrame(data = conditions) 
pca_df = pd.DataFrame(data = pca_out, columns = ["PCA1", "PCA2", "PCA3", "PCA4", "PCA5", "PCA6"]) 
condition_labelled_Df = pd.concat([pca_df, condition_df], axis=1)
print(condition_labelled_Df)

#Scatter plot of PCA1 and PCA2 
fig, ax = plt.subplots(figsize=(6,6))
for n, grp in condition_labelled_Df.groupby('conditions'):
    ax.scatter(x = "PCA1", y = "PCA2", data=grp, label=n)
ax.legend(title="Genotype", fontsize="large", title_fontsize="large")
plt.xlabel(f"PC1 ({PC1_expvar}% explained var.)", fontsize="large")
plt.ylabel(f"PC2 ({PC2_expvar}% explained var.)", fontsize="large")
plt.title(plot_title, fontsize="xx-large")
plt.savefig(fig_filename)








