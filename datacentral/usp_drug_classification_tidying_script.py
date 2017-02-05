#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Parse and tidy the USP Drug Classification data from KEGG
Raw data from http://www.genome.jp/kegg-bin/get_htext?htext=br08302.keg

Created on Sun Feb  5 13:15:04 2017

@author: claire
"""

import numpy as np
import pandas as pd

if __name__ == "__main__":
    
    fname = 'br08302.keg'
    with open(fname, 'r') as f:
        all_lines = f.readlines()
        
    usp = []
    for line in all_lines:
        if line.startswith('A'):
            current_category = line.strip()[1:]
        elif line.startswith('B'):
            current_class = line[1:].strip()
        elif line.startswith('C'):
            current_drug = line[1:].split('[')[0].strip()
            try:
                current_drug_id = line[1:].split(':')[1].strip(']\n')
            except:
                current_drug_id = np.nan
        elif line.startswith('D'):
            line = line[1:].strip()
            # The KEGG ID is the first 6 characters (after the 'D')
            example_drug_id = line[0:6]
            # The drug name is after the KEGG ID and before parentheses (if any)
            example_drug_name = line[6:].strip().split('(')[0].strip()
            if line.endswith(')'):
                nomenclature = '(' + line.split('(')[-1]
            else:
                nomenclature = np.nan
            usp.append([current_category, current_class, current_drug,
                        current_drug_id, example_drug_name,
                        example_drug_id, nomenclature])
    
    uspdf = pd.DataFrame(usp, columns=['usp_category', 'usp_class', 'usp_drug',
                                     'kegg_id_drug', 'drug_example',
                                     'kegg_id_drug_example', 'nomenclature'])
    uspdf.to_csv('usp_drug_classification.csv', index=False)