#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd


def build_tissue_and_gene_lists(
    df_genes: pd.DataFrame,
    p: dict
) -> dict:

    """Build lists and dictionaries with tissue and mask names."""

    c = dict()

    # Genes
    gene_names_iss = list(df_genes['gene_iss'].unique())  # gene names analyzed with in-situ sequencing
    gene_names_iss.sort()  # sort genes alphabetically
    c['gene_names_iss'] = gene_names_iss

    ####

    # Tissue masks and rgb-colors
    c['tissue_names_mask'] = ['neoplastic', 'non-neoplastic']  # tissue names for mask building

    c['tissue_mask_names'] = ["tissue '" + mask_name + "'" for mask_name in c['tissue_names_mask']]  # names of tissue masks

    # Tissue region masks (boundary and center)
    c['tissue_region_masks_dict'] = {mask_name: {'boundary': mask_name + ' boundary', 'center': mask_name + ' center'}
                                     for mask_name in c['tissue_mask_names']
                                     if any(["'" + tissue_name + "'" in mask_name
                                     for tissue_name in p['tissue_region_masks']['tissues']])}
    c['tissue_region_mask_names'] = sum([list(c['tissue_region_masks_dict'][k].values())
                                         for k in c['tissue_region_masks_dict'].keys()], [])  # all mask names

    ####

    # All tissue masks for bar plot
    c['tissue_mask_names_calc'] = c['tissue_mask_names'] + \
                                  c['tissue_region_mask_names']  # tissue masks for calculation

    ####
    
    c['all_tissue_mask_names_calc'] = ['gene ' + mask_name for mask_name in c['tissue_mask_names_calc']] + \
                                      ['drawn ' + mask_name for mask_name in c['tissue_mask_names_calc']]

    ####

    # Gene sets with title for custom plots
    c['custom_gene_set_names'] = list(p['custom_gene_sets'].keys())  # custom gene sets

    ####

    # Units for statistics
    c['units'] = ['[-]', 'per cell [-]', 'per area [um-2]']

    return c

#################################
