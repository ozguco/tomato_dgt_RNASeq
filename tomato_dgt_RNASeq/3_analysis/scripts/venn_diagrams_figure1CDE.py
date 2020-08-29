#!/usr/bin/env python
from matplotlib_venn import venn2_unweighted
from matplotlib import pyplot as plt
import os, sys 

#This script creates a 2-circle venn diagram comparing expressed genes from the same tissue type in two different genotypes
#Use D_only, E_only, and M_only gene lists from output of venn_diagrams_figure1AB.py
#Run with AC file location in the first position, then dgt file next (see usage statement)

#Usage statement 
usage = 'Usage: ' + sys.argv[0] + " <AC_filepath> <dgt_filepath>"
if len(sys.argv) != 3: 
    print('Exiting: ' + usage)
    sys.exit()
elif ('AC' not in sys.argv[1]) or ('dgt' not in sys.argv[2]): 
    print(usage)

#Functions -- gene names must be in first column of input file
def readGeneList(file): 
    genenames = []
    F = open(file)
    for line in F: 
        terms = line.strip().split('\t')
        genenames.append(terms[0])
    F.close()
    return genenames 

###Input filename format 'D_only_dgt_TPMgreater_2.0.txt'
def findOutputFilename(file): 
    pathparts = file.split('/')
    filename = pathparts[-1]
    name_nofiletype = (filename.rsplit('.', 1))[0]
    name_parts = name_nofiletype.split('_')
    cutoff_id = '_'.join(name_parts[-2:])
    zone_id = name_parts[0]
    return cutoff_id, zone_id

#Process input files and prepare file names/locations for output
WT_filepath = sys.argv[1]
dgt_filepath = sys.argv[2]
venn_output_location = '../figures'
genelist_output_location = '../gene_lists'

namingscheme_parts = list(findOutputFilename(WT_filepath))
WT_cutoff_id = namingscheme_parts[0]
WT_zone_id = namingscheme_parts[1]
venn_output_filename = 'fig1_' + WT_zone_id + '_' + WT_cutoff_id + '.png'

WT_expr = set(readGeneList(WT_filepath))
dgt_expr = set(readGeneList(dgt_filepath))

zone_id_key = {'D': 'Differentiation Zone', 'E': 'Elongation Zone',\
'M': 'Meristem'}
zone = zone_id_key[WT_zone_id]

#Generate venn diagram
venn = venn2_unweighted ([WT_expr, dgt_expr], set_labels=("WT", "dgt"))
plt.title(str(zone))
plt.savefig(os.path.join(venn_output_location, venn_output_filename))

#Create gene lists for each section of venn diagram
intersections_dict = {'WT_dgt': WT_expr.intersection(dgt_expr),\
'WT_only': WT_expr.difference(dgt_expr), 'dgt_only': dgt_expr.difference(WT_expr)}

for inter_key in intersections_dict: 
    filename = inter_key + '_' + WT_zone_id + '_' + WT_cutoff_id + '.txt'
    filepath = os.path.join(genelist_output_location, filename)
    IF = open(filepath, 'w')
    for member in intersections_dict[inter_key]: 
        IF.write(member + '\n')
    IF.close()

