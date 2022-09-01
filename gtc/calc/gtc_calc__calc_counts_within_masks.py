#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.function as g_fct


def calc_counts_within_masks(
    masks: dict,
    df_counts: pd.DataFrame,
    df_cells: pd.DataFrame,
    df_genes: pd.DataFrame,
    c: dict,
    p: dict
) -> None:

    """Calculate the absolute frequency of the cells and
    genes of each gene type in the previously created masks.
    If normalization is performed, then the counts of the
    for normalization used gene is calculated in all tissues
    which defined in Gtc_Parameters.txt"""

    gene_names_iss = c['gene_names_iss']
    tissue_mask_names_calc = c['all_tissue_mask_names_calc']

    ####

    def calc_counts(row_name, coord_x, coord_y):
        df_col_names = g_fct.df_col_names(tissue_mask_names_calc, c['units'][0])

        for mask_name, col_name in zip(tissue_mask_names_calc, df_col_names):
            within = [masks[mask_name][x, y] == 255 for x, y in zip(coord_x, coord_y)]

            df_counts.loc[row_name, col_name] = sum(within)

    ##

    calc_counts('cells', df_cells['row'], df_cells['col'])  # count cells

    for gene_name in gene_names_iss:  # count genes
        df_gene = df_genes[df_genes['gene_iss'] == gene_name]  # filter genes of one type

        calc_counts(gene_name, df_gene['row'], df_gene['col'])

    ####

    # print('-Perform count normalization: %s' % perform_count_normalization)
    #
    # if perform_count_normalization == 'yes':  # perform normalization with gene defined in 'Gtc_Parameters.txt'
    #
    #     tissue_mask_names_norm = c['tissue_mask_names']  # all in 'Gtc_Parameters.txt' defined tissues are used for the calculation of the normalization factor
    #     perform_count_normalization = p['count_normalization']['perform']
    #     gene_name_for_norm = p['count_normalization']['gene']
    #
    #     if gene_name_for_norm not in gene_names_iss: raise ValueError("Gene name defined in 'Gtc_Parameters.txt' "
    #                                                                   "for normalization is not part of 'gene_pos_csv'")
    #
    #     for mask_type in ['gene', 'drawn']:
    #         mask_names = [mask_type + ' ' + mask_name for mask_name in tissue_mask_names_norm]
    #         col_names = g_fct.df_col_names(mask_names, c['units'][0])
    #
    #         norm_factor = df_counts.loc[gene_name_for_norm, col_names].sum()  # sum over tissue mask columns
    #
    #         print('-For gene %s a normalization factor of %d is calculated in all %s tissue masks'
    #               % (gene_name_for_norm, norm_factor, mask_type))
    #
    #         df_counts.loc[gene_names_iss, col_names] = df_counts.loc[gene_names_iss, col_names].div(norm_factor)

    ####

    # df_counts['Counts in "all tissue" masks [-]'] = \
    #     df_counts[df_col_names(tissue_mask_names, units[0])].sum(axis=1)  # sum over tissue mask columns

#################################
