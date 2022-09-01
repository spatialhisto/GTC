#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import pandas as pd
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.function as g_fct


def plot_positions_of_cells_and_used_genes_for_gene_mask_building(
    orig_img_props: dict,
    masks: dict,
    df_cells: pd.DataFrame,
    df_genes: pd.DataFrame,
    p: dict
):

    """Plot positions in colors of combined mask for:
     - all cells and for all genes used to build the composite gene mask
     - the genes of the gene types used to build the gene masks
       neoplastic and connective in tumor."""

    dot_radius = p['plot_props']['dot_radius']

    ####

    def plot_pos_and_save(df, file_name):
        img_tmp = g_msk.new_white_color_image(orig_img_props['dims'])  # empty black binary image

        for row_gene, col_gene in zip(df['row'], df['col']):
            color_bgr = masks['gene combined masks'][row_gene, col_gene]  # get tissue color for position
            color_bgr = tuple([int(x) for x in color_bgr])  # convert color in integer tuple format
            cv2.circle(img_tmp, g_fct.switch_coordinates((row_gene, col_gene)), dot_radius, color_bgr, thickness=cv2.FILLED)  # draw dot

        g_plt.save_resized_image(orig_img_props, img_tmp, file_name, p)  # plot small image

    ####

    plot_pos_and_save(df_cells, 'Control_plot_all cells')  # cell positions
    plot_pos_and_save(df_genes, 'Control_plot_all genes')  # all gene positions

    ####

    tissues = ['neoplastic']

    for tissue in tissues:  # for tissues used to mask building with genes
        gene_set = p['tissue_masks'][tissue]['genes']  # genes used to build tissue masks

        for gene in gene_set:
            df_gene = df_genes[df_genes['gene_iss'] == gene]  # filter genes of specific type

            plot_pos_and_save(df_gene, 'Control_plot_gene mask_' + gene)  # gene positions of gene sets used for tissue mask building

#################################
