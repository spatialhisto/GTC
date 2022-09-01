#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd


def check_if_param_genes_are_within_df_genes(
    df_genes: pd.DataFrame,
    p: dict
):

    """Check if genes from the gtc parameter are in the gene location dataframe."""

    genes_of_df = pd.Series(df_genes['gene_iss'])

    genes_of_gtc_param_file = p['tissue_masks']['neoplastic']['genes'] + \
                              sum([*p['custom_gene_sets'].values()], [])

    for gene in genes_of_gtc_param_file:
        if not any(genes_of_df.isin([gene])):
            raise ValueError("The gene %s is not in the 'gene_pos_csv' file"
                             "- Check the gene name in 'Gtc-Parameters'!" % gene)

#################################
