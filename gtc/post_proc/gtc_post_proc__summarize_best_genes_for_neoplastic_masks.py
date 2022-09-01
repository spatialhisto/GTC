#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import re
import pandas as pd
import gtc.post_proc as g_post


def summarize_best_genes_for_neoplastic_masks(
    df_overlap: dict
) -> pd.DataFrame:

    """Summarize the best
    genes in a data frame."""

    names_gtc_param = list(df_overlap['name_gtc_param'])
    genes_used_in_masks = {ngp: re.split('Gtc_Parameters|_', ngp) for ngp in names_gtc_param}
    genes_used_in_masks = {k: v[2] for (k, v) in genes_used_in_masks.items() if len(v) > 2}
    genes_used_in_masks = {k: re.split('-', v) for (k, v) in genes_used_in_masks.items()}

    genes_all = list()
    genes_all = [genes_all + v for (_, v) in genes_used_in_masks.items()]  # combine values of dict
    genes_all = sum(genes_all, [])  # flatten list
    genes_all = list(set(genes_all))  # make list unique
    genes_all.sort()

    df = pd.DataFrame(' ',
                      index=range(len(df_overlap.index)),
                      columns=['rank', 'geometric_mean', 'name_gtc_param'] + genes_all)
    df['rank'] = df_overlap['rank']
    df['geometric_mean'] = df_overlap['geometric_mean']
    df['name_gtc_param'] = df_overlap['name_gtc_param']

    for (name_gtc_param, genes) in genes_used_in_masks.items():
        index = g_post.get_row_index(df, 'name_gtc_param', name_gtc_param)
        for gene in genes:
            df.at[index, gene] = 'x'

    df = df.sort_values(by=['rank'], ascending=True)

    return df

#################################
