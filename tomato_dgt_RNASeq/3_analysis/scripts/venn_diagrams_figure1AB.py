#!/usr/bin/env python
from matplotlib_venn import venn3_unweighted
from matplotlib import pyplot as plt
import os, sys

#This script creates a 3-circle Venn diagram comparing expressed (based on presence-abscence call) genes from each tissue for a given genotype
#Naming is important, the script should use file outputs from 1_quantitate_transcripts/3_find_expressed_genes with specific input filename format (specified below)
#You will need to rerun this script with appropriate files for each 3-circle Venn diagram you are creating.

#Usage statement 
usage = 'Usage: ' + sys.argv[0] + " <D_GeneList_filepath> <E_GeneList_filepath> <M_GeneList_filepath>"
if len(sys.argv) != 4: 
    print(usage)
    sys.exit()
elif ('D' not in sys.argv[1]) or ('E' not in sys.argv[2]) or ('M' not in sys.argv[3]): 
    print(usage)

#Functions -- right now, works with gene_id in the first position, anything in other positions 
def readExpressedGenes(file): 
    genenames = [] 
    F = open(file)
    F.readline()
    for line in F: 
        terms = line.strip().split('\t')
        genenames.append(terms[0])
    F.close()
    return genenames 

###Input filename format '[SOMETHING]_dgt_D_all_TPMgreater_2.0.txt' 
def findOutputFilename(file): 
    pathparts = file.split('/')
    filename = pathparts[-1]
    name_nofiletype = (filename.rsplit('.', 1))[0]
    name_parts = name_nofiletype.split('_')
    cutoff_id = '_'.join(name_parts[-2:])
    plant_id = name_parts[-5]
    output_name = 'fig1_' + plant_id + '_' + cutoff_id + '.png'
    return output_name, cutoff_id, plant_id 

#Process input files and prepare file names/locations for output
D_filepath = sys.argv[1]
E_filepath = sys.argv[2]
M_filepath = sys.argv[3]
venn_output_location='../figures'
genelist_output_location='../gene_lists'
namingscheme_parts = list(findOutputFilename(D_filepath))
venn_output_filename = namingscheme_parts[0] 
D_cutoff_id = namingscheme_parts[1]
D_plant_id = namingscheme_parts[2]

if D_plant_id == 'AC': 
    plant_type = 'WT'
elif D_plant_id =='dgt': 
    plant_type = 'dgt'

TPM_value = D_cutoff_id.split('_')[-1]

D_expr = set(readExpressedGenes(D_filepath))
E_expr = set(readExpressedGenes(E_filepath))
M_expr = set(readExpressedGenes(M_filepath))

#Generate venn diagram
venn = venn3_unweighted([D_expr, E_expr, M_expr], set_labels=("Differentiation", "Elongation", "Meristem"))
plt.title(f"Expressed Genes TPM > {TPM_value} ({plant_type})")
plt.savefig(os.path.join(venn_output_location, venn_output_filename))

#Create gene lists for each section of venn diagram
intersections_dict = {'DEM': D_expr.intersection(E_expr).intersection(M_expr), 'DE_only': D_expr.intersection(E_expr).difference(M_expr),\
'EM_only': E_expr.intersection(M_expr).difference(D_expr), 'DM_only': D_expr.intersection(M_expr).difference(E_expr),\
'D_only': D_expr.difference(E_expr).difference(M_expr), 'E_only': E_expr.difference(D_expr).difference(M_expr),\
'M_only': M_expr.difference(D_expr).difference(E_expr)}

for inter_key in intersections_dict: 
    filename = inter_key + '_' + D_plant_id + '_' + D_cutoff_id + '.txt' 
    filepath = os.path.join(genelist_output_location, filename)
    IF = open(filepath, 'w')
    for member in intersections_dict[inter_key]: 
        IF.write(member + '\n')
    IF.close()
