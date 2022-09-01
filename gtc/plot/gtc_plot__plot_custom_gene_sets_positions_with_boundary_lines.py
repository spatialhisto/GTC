#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################
import numpy as np
import pandas as pd
import gtc.mask as g_msk
import matplotlib.pyplot as plt


def plot_custom_gene_sets_positions_with_boundary_lines(
    mask_boundary_lines: np.ndarray,
    df_genes: pd.DataFrame,
    c: dict,
    p: dict,
    alpha_img: float = 0.4,
    alpha_plot: float = 1.0,
    leg_font_size: int = 8
):

    """Plot genes of the defined gene sets on tissue mask image."""

    dot_radius = p['plot_props']['dot_radius']
    gene_sets = p['custom_gene_sets']
    img_res_in_dpi = p['img_res_in_dpi']

    ####

    mask_boundary_lines = g_msk.invert_binary_mask(mask_boundary_lines)  # inverted tissue border lines

    ####

    def sort_genes_by_frequency():
        df_set = df_genes[df_genes['gene_iss'].isin(gene_sets[gene_set_name])]['gene_iss']
        counts = df_set.value_counts()
        counts.sort_values(inplace=True, ascending=False)
        sorted_genes = list(counts.index)

        return sorted_genes

    ####

    for gene_set_name in c['custom_gene_set_names']:
        print("-Plot positions of gene set '%s'" % gene_set_name)

        sorted_genes = sort_genes_by_frequency()  # plot low occurring genes over high occurring genes - avoid cover

        fig, ax = plt.subplots()  # new plot
        fig.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
        ax.imshow(mask_boundary_lines, alpha=alpha_img, interpolation='gaussian')  # new background image to plot on

        for gene in sorted_genes:  # loop over all genes in custom gene set
            df_gene = df_genes[df_genes['gene_iss'] == gene]  # select gene of one type

            plt.scatter(df_gene['col'], df_gene['row'], marker='.', s=dot_radius, label=gene,  # !!!NOTE: switched x- and y-coordinates
                        alpha=alpha_plot, zorder=-1)  # plot boundary lines over scatter plot

        ax.axis('off')
        fig.patch.set_visible(False)
        plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1.1, 0.5), prop={'size': leg_font_size})
        plt.savefig(p['output'] + 'Plot_positions_of_gene_set_' + gene_set_name + '.png', dpi=img_res_in_dpi)
        plt.close('all')

#################################
