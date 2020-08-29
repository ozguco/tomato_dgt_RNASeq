#!/usr/bin/env python 
from matplotlib_venn import venn3_unweighted
from matplotlib import pyplot as plt
import os, sys 

#This script creats a 3-circle Venn diagram comparing differentially expressed genes (dgt vs WT) in different tissues
#Takes in upregulated/downregulated gene sets (DGT compared to WT). 
#Naming format is important, use the file outputs from 2_differential_gene_expression/3_find_upreg_downreg.sh with specific input filename format (specified below)

#Named as:
#[SOMETHING]_PPDE1.0_postFCgreater2.0.txt 
#[SOMETHING]_PPDE1.0_postFCless0.5.txt 

#Usage statement 
usage = 'Usage: ' + sys.argv[0] + " <D_GeneList_filepath> <E_GeneList_filepath> <M_GeneList_filepath>"
if len(sys.argv) != 4: 
    print(usage)
    sys.exit()
elif ('D' not in sys.argv[1]) or ('E' not in sys.argv[2]) or ('M' not in sys.argv[3]): 
    print(usage)

#Functions -- gene names must be in first column of input file
def readExpressedGenes(file): 
    genenames = [] 
    F = open(file)
    F.readline() 
    for line in F: 
        terms = line.strip().split('\t')
        genenames.append(terms[0])
    F.close()
    return genenames 

#Input filename format '[SOMETHING]_PPDE1.0_postFCless0.5.txt' or '[SOMETHING]_PPDE1.0_postFCgreater2.0.txt' 
def findOutputFilename(file): 
    pathparts = file.split('/')
    filename = pathparts[-1]
    name_nofiletype = (filename.rsplit('.', 1))[0]
    name_parts = name_nofiletype.split('_')
    PPDE = name_parts[-2]
    postFC = name_parts[-1]
    if 'greater' in postFC: 
        updown_ID = 'Upregulated'
        inequality_sym = '>'
    elif 'less' in postFC: 
        updown_ID = 'Downregulated'
        inequality_sym = '<'
    else: 
        print('Naming error')
    return PPDE, postFC, updown_ID, inequality_sym

#Process input files and prepare file names/locations for output
D_filepath = sys.argv[1]
E_filepath = sys.argv[2]
M_filepath = sys.argv[3]
venn_output_location='../figures'
genelist_output_location='../gene_lists'
namingscheme_parts = list(findOutputFilename(D_filepath))
D_PPDE = namingscheme_parts[0]
D_postFC = namingscheme_parts[1]
D_updown_ID = namingscheme_parts[2]
venn_output_filename = 'fig2_' + D_updown_ID + '_' + D_PPDE + '_' + D_postFC + '.png'

PPDE_value = (D_PPDE.split('PPDE'))[-1]
D_inequality_sym = namingscheme_parts[3]
postFC_value = (D_postFC.split('greater')[-1]).split('less')[-1]

D_expr = set(readExpressedGenes(D_filepath))
E_expr = set(readExpressedGenes(E_filepath))
M_expr = set(readExpressedGenes(M_filepath))

#Generate venn diagram
venn = venn3_unweighted([D_expr, E_expr, M_expr], set_labels=("Differentiation", "Elongation", "Meristem"))
plt.title(f"DGT {D_updown_ID} As Compared to WT (PPDE = {PPDE_value} and postFC {D_inequality_sym} {postFC_value})") 
plt.savefig(os.path.join(venn_output_location, venn_output_filename))

#Create gene lists for each section of venn diagram
intersections_dict = {'DEM': D_expr.intersection(E_expr).intersection(M_expr), 'DE_only': D_expr.intersection(E_expr).difference(M_expr),\
'EM_only': E_expr.intersection(M_expr).difference(D_expr), 'DM_only': D_expr.intersection(M_expr).difference(E_expr),\
'D_only': D_expr.difference(E_expr).difference(M_expr), 'E_only': E_expr.difference(D_expr).difference(M_expr),\
'M_only': M_expr.difference(D_expr).difference(E_expr)}

for inter_key in intersections_dict: 
    filename = inter_key + '_' + D_updown_ID + '_' + D_PPDE + '_' + D_postFC + '.txt' 
    filepath = os.path.join(genelist_output_location, filename)
    IF = open(filepath, 'w')
    for member in intersections_dict[inter_key]: 
        IF.write(member + '\n')
    IF.close()