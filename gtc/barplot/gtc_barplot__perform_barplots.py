#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.barplot as g_bar
import matplotlib.pyplot as plt


def perform_barplots(
    df_counts: pd.DataFrame,
    mask_type: str,
    c: dict,
    p: dict
):

    """Plot grouped and stacked bar plots either for all genes or for a custom
    subset of the genes defined in the parameters file."""

    masks_to_plot = [mask_type + ' ' + mask_name for mask_name in c['tissue_mask_names_calc']]  # define mask names to plot

    ####

    def call_barplot_funcs(masks_to_plot, df, title):
        if barplot_type == 'grouped':
            g_bar.plot_grouped_barplots(masks_to_plot, df, mask_type + ' ' + 'tissue', unit, title, p)
        else:
            g_bar.plot_stacked_barplots(masks_to_plot, df, mask_type + ' ' + 'tissue', unit, title, p)
        plt.close('all')

    ####

    for barplot_type in ['grouped', 'stacked']:

        for unit in c['units']:  # plot all genes
            print('-Plot ' + barplot_type + ' bar plot with counts %s' % unit)
            call_barplot_funcs(masks_to_plot, df_counts, 'Gene Expression Counts')

        ####

        for set_name in c['custom_gene_set_names']:  # plot custom gene sets
            set_genes = p['custom_gene_sets'][set_name]
            df_set = df_counts[df_counts['genes'].isin(set_genes)]
            df_set.reset_index(drop=True, inplace=True)

            for unit in c['units']:
                print("-Plot " + barplot_type + " bar plot for '" + set_name + "' with counts %s" % unit)
                call_barplot_funcs(masks_to_plot, df_set, set_name)

#################################
