#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################
#

import cv2
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.calc as g_calc
import gtc.setup as g_set
import gtc.barplot as g_bar
import gtc.control as g_ctrl
import gtc.function as g_fct


def main_function(
    fname_gtc_param: str,
    DEBUG: bool = False
) -> None:

    """The main function for counting genes in masks."""

    ##################
    print('*** Setup')
    ##################

    g_set.create_output_dir(fname_gtc_param)  # create output directory if not existing

    log_file_name = g_set.assemble_output_dirname(fname_gtc_param) + 'Report.txt'  # start output Logger
    g_set.start_logging(log_file_name)

    ##################################
    print('*** Create gtc parameters')
    ##################################

    p = g_set.create_and_edit_gtc_param(fname_gtc_param)  # load gtc parameter settings

    ############################################
    print('*** Import csv data and check genes')
    ############################################

    df_genes = g_set.read_csv_data(p['files']['gene_pos_csv'], ['gene_iss', 'col', 'row'],  # !!!NOTE reversed order of row and col
                                   [], p['img_scale_factor'])
    df_cells = g_set.read_csv_data(p['files']['cell_pos_csv'], ['col', 'row'],  # !!!NOTE reversed order of row and col
                                   [], p['img_scale_factor'])

    g_ctrl.check_if_param_genes_are_within_df_genes(df_genes, p)

    #####################################################
    print('*** Build tissue and unique gene names lists')
    #####################################################

    c = g_set.build_tissue_and_gene_lists(df_genes, p)
    print('The panel contains %d genes: %s' % (len(c['gene_names_iss']), ', '.join(c['gene_names_iss'])))

    ###########################################################
    print('*** Import microscope images and drawn tissue mask')
    ###########################################################

    masks = dict()  # dictionary that contains all the masks and images

    masks['orig dapi image'] = g_msk.create_and_scale_original_image('dapi_image_tif', p)
    masks['orig fitc image'] = g_msk.create_and_scale_original_image('fitc_image_tif', p)

    masks['orig drawn tissue mask image'] = cv2.imread(p['files']['drawn_tissue_mask_png'])

    ##################################################
    print('*** Calculate microscope image dimensions')
    ##################################################

    orig_img_props = g_set.calc_image_dims(masks['orig dapi image'], p)

    #####################################
    print('*** Create virtual H&E image')
    #####################################

    masks['virtual H&E image'] = g_msk.create_virtual_he_image_method2(orig_img_props, masks)

    #########################################################
    print('*** Remove genes from csv data in specific areas')
    #########################################################

    df_genes = g_msk.remove_genes_from_csv_data_for_specific_areas(orig_img_props, masks, df_genes)  # remove genes

    ####################################
    print('*** Create secure seal area')
    ####################################

    masks['secure seal area'] = g_msk.create_secure_seal_area_mask(orig_img_props, p)  # only genes within this mask are valid to count

    ##################################
    print('*** Create masks by genes')
    ##################################

    print("-Create gene mask for tissue 'composite'")
    masks["gene tissue 'composite'"] = g_msk.create_tissue_composite_mask(orig_img_props, masks, df_cells, df_genes, p, DEBUG)  # create a mask for entire tissue based on gene and cell positions

    print("-Create gene mask for 'neoplastic'")
    masks["gene tissue 'neoplastic'"] = g_msk.create_tissue_mask(orig_img_props, masks, df_genes, 'neoplastic', p)  # create tissue mask

    print("-Create gene mask for 'non-neoplastic'")
    masks["gene tissue 'non-neoplastic'"] = g_msk.create_tissue_non_neoplastic_mask(masks)  # create a mask for entire tissue based on gene and cell positions

    print('-Create gene tissue boundary and tissue center masks')
    g_msk.create_tissue_boundary_and_center_masks(masks, 'gene', c, p)  # create a boundary+center mask for each tissue defined in the parameter file
    masks['gene boundary lines tissues'] = g_msk.create_tissue_boundary_lines_mask(orig_img_props, masks, 'gene', c, p)  # mask with tissue border lines

    print('-Combine gene tissue masks in one image')
    masks['gene combined masks'] = g_msk.create_combined_tissue_masks(orig_img_props, masks, 'gene', c)

    ####################################
    print('*** Create masks by drawing')
    ####################################

    print("-Create drawn mask for tissue 'neoplastic'")
    masks["drawn tissue 'neoplastic'"] = g_msk.create_tissue_masks_from_drawing(orig_img_props, masks, 'neoplastic', p)

    print("-Create drawn mask for tissue 'non-neoplastic'")
    masks["drawn tissue 'non-neoplastic'"] = g_msk.create_tissue_masks_from_drawing(orig_img_props, masks, 'non-neoplastic', p)

    print('-Create drawn tissue boundary and tissue center masks')
    g_msk.create_tissue_boundary_and_center_masks(masks, 'drawn', c, p)  # create a boundary+center mask for each tissue defined in the parameter file
    masks['drawn boundary lines tissues'] = g_msk.create_tissue_boundary_lines_mask(orig_img_props, masks, 'drawn', c, p)  # mask with tissue border lines

    print('-Combine drawn tissue masks in one image')
    masks['drawn combined masks'] = g_msk.create_combined_tissue_masks(orig_img_props, masks, 'drawn', c)

    ###################################################################################
    print('*** Calculate overlap and draw overlap of both masks for neoplastic tissue')
    ###################################################################################

    overlap = g_calc.calc_overlap_neoplastic_tissue_in_drawn_and_gene_build_masks(masks)
    print('-Neoplastic tissue in gene build mask and drawn mask has overlap of: %1.3f' % round(overlap, 3))

    masks["overlap tissue 'neoplastic' masks"] = g_msk.create_overlap_neoplastic_tissue_masks_image(orig_img_props, masks)

    #######################
    print('*** Plot masks')
    #######################

    g_plt.plot_all_masks(orig_img_props, masks, p, DEBUG)  # plot all tissue masks

    g_plt.plot_blend_yellow_mask_over_orig_img(orig_img_props, masks, 'gene', c, p)  # blend yellow colored masks over the original microscope image

    g_plt.plot_blend_mask_over_orig_img(orig_img_props, masks, 'gene combined masks', p)  # blend a mask over the original microscope image
    g_plt.plot_blend_mask_over_orig_img(orig_img_props, masks, 'drawn combined masks', p)

    ##########################################################################
    print('*** Plot cells, genes and gene sets used for tissue mask building')
    ##########################################################################

    g_plt.draw_df_coords_with_mask_colors(orig_img_props, masks, 'gene', df_cells, 'cells', c, p)  # perform control plot of cells in tissue masks

    g_plt.plot_custom_gene_sets_positions_with_boundary_lines(masks['gene boundary lines tissues'], df_genes, c, p)

    ####################################################################################
    print('*** Custom plot 2d-histogram and contourf plot of genes with boundary lines')
    ####################################################################################

    g_plt.plot_custom_gene_sets_hist2d_and_contourf_with_boundary_lines(masks, df_genes, c, p)  # plot 2d-histogram of custom gene sets

    #############################################################
    print('*** Control: Check that masks only contain 0s and 1s')
    #############################################################

    g_ctrl.control_all_masks_contains_only_0_and_1(masks, c)

    g_plt.plot_positions_of_cells_and_used_genes_for_gene_mask_building(orig_img_props, masks, df_cells, df_genes, p)

    ##################################################################################################
    print('*** Calculate cell and gene counts within tissue masks (absolute, per cells and per area)')
    ##################################################################################################

    df_counts = g_calc.create_df_for_count_statistics(c)
    g_calc.calc_counts_within_masks(masks, df_counts, df_cells, df_genes, c, p)  # calculate counts of cells and genes within masks

    g_calc.calc_counts_per_cell(df_counts, c)  # calculate counts per cell

    g_calc.calc_counts_per_area(orig_img_props, masks, df_counts, c)  # calculate counts per mask area

    df_counts.to_csv(p['output'] + 'Count_matrix.csv', index=True, sep=';', decimal=',')  # save results to csv
    g_fct.prepare_df_for_plots(df_counts)  # re-arrange dataframe for bar plots

    ##################################################
    print('*** Plot polar chart of gene count ratios')
    ##################################################

    g_plt.plot_polar_chart_gene_count_ratios(df_counts, p, DEBUG)

    ######################################################################################################
    print('*** Plot grouped bar plots, stacked bar plots and top gene expression barplots of mask counts')
    ######################################################################################################

    g_bar.plot_top_gene_expression_barplots(df_counts, c, p)  # plot top gene expressions in masks as bar plot
    g_bar.perform_barplots(df_counts, 'gene', c, p)  # plot grouped and stacked bar plots for all genes and custom gene sets

    ############################
    print('*** End of analysis')
    ############################

    g_set.stop_logging()  # stop logger

#################################
