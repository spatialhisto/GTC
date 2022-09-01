#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.post_proc as g_post


def perform_post_processing(
    main_output_dir: str,
    paths_samples: list,
    path_df_pathways_csv: str,
    DEBUG: bool = False
) -> None:

    """Perform the post processing of the analysis."""

    ONLY_FOR_COUNTS_PER_CELL = True
    ONLY_FNAMES_GTC_PARAM_WITH_TOP_RANKS = True
    num_top_ranks = 20

    ####

    fnames_to_copy = ["Plot_mask_or_img_drawn combined masks.png",
                      "Plot_mask_or_img_gene combined masks.png",
                      "Plot_mask_or_img_overlap tissue 'neoplastic' masks.png",
                      "Plot_polar_chart_gene_count_ratios.png",
                      "Plot_blend_drawn combined masks.png",
                      "Plot_blend_gene combined masks.png",
                      "Count_matrix.csv",
                      "Report.txt"]

    ####

    fnames_gtc_param = g_post.detect_fnames_of_gtc_param_files_present_in_all_sample_dirs(main_output_dir, paths_samples, DEBUG)  # Gtc_Parameters_... files present in all sample paths

    dict_disease_history = g_post.create_dict_disease_history(main_output_dir, paths_samples, fnames_gtc_param, DEBUG)  # load the patient history relaps yes/no

    df_pathway_groups = pd.read_csv(path_df_pathways_csv, sep=',')  # load the processes correlated with the iss genes

    #######################
    print('*** Copy files')
    #######################

    g_post.backup_original_gtc_parameters_files(main_output_dir, paths_samples, fnames_gtc_param)
    g_post.copy_files_into_same_folder(main_output_dir, paths_samples, fnames_gtc_param, fnames_to_copy)  # copy all files specified in fnames_to_copy in the same folder

    ###############################
    print('*** Calculate overlaps')
    ###############################

    df_overlap = g_post.summarize_overlaps_neoplastic_masks(main_output_dir, paths_samples, fnames_gtc_param)  # calculate overlap for all cases and samples
    df_overlap.to_csv(main_output_dir + 'Summary_overlaps.csv', index=False, sep=';', decimal=',')

    df_best_genes = g_post.summarize_best_genes_for_neoplastic_masks(df_overlap)
    df_best_genes.to_csv(main_output_dir + 'Summary_best_genes.csv', index=False, sep=';', decimal=',')

    names_gtc_param_ranks = g_post.create_dict_names_gtc_param_ranks(df_overlap)  # build dictionary with the rank assigned to the names_gtc_param

    #############################################
    print('*** Summarize images for all samples')
    #############################################

    fnames_images = [fname_image for fname_image in fnames_to_copy if '.png' in fname_image]

    if len(paths_samples) > 1:
        for fname_image in fnames_images:
            print('-For image: ' + fname_image)
            g_post.plot_images_for_all_samples(main_output_dir, paths_samples, fnames_gtc_param,
                                               dict_disease_history, df_overlap, fname_image)

    ###############################################################################
    print('*** Summarize images for all samples of single Gtc_Parameters.txt file')
    ###############################################################################

    if len(paths_samples) > 1:
        g_post.plot_images_for_all_samples_for_single_gtc_param(main_output_dir, paths_samples, fnames_gtc_param,
                                                                dict_disease_history, df_overlap, fnames_images)

    ####################################################################################################
    print('*** Limit the number of fnames_gtc_param for further post processing to the highest ranking')
    ####################################################################################################

    if ONLY_FNAMES_GTC_PARAM_WITH_TOP_RANKS: fnames_gtc_param = g_post.limit_number_of_fnames_gtc_param(df_overlap, num_top_ranks)  # only perform further post-processing for top rank cases

    #############################################
    print('*** Summarize count matrix csv-files')
    #############################################

    genes, column_names = g_post.analyze_structure_count_matrix_files(main_output_dir)

    if ONLY_FOR_COUNTS_PER_CELL: column_names = [column_name for column_name in column_names if 'per cell' in column_name]  # only perform further post-processing for counts per cell [-]

    dfs_counts = g_post.summarize_count_matrix(main_output_dir, paths_samples, fnames_gtc_param, genes, column_names)
    g_post.save_excel_files_for_counts(main_output_dir, fnames_gtc_param, column_names, dfs_counts)

    ####################################
    print('*** Barplot the mean counts')
    ####################################

    g_post.plot_barplot_mean_gene_counts_for_tissues(main_output_dir, fnames_gtc_param, genes,
                                                     column_names, dfs_counts, names_gtc_param_ranks)

    g_post.plot_barplot_mean_gene_counts_for_relaps(main_output_dir, fnames_gtc_param, genes, column_names,
                                                    dict_disease_history, dfs_counts, names_gtc_param_ranks)

    ##############################################################
    print('*** Perform t-test calculations and summarize results')
    ##############################################################

    if len(paths_samples) > 1:
        dfs_stat = g_post.summarize_t_tests(fnames_gtc_param, genes, column_names, dict_disease_history, dfs_counts)
        g_post.save_excel_files_for_statistics(main_output_dir, fnames_gtc_param, column_names, dfs_stat)

    ################################################
    print('*** Vulcano plot for gene distributions')
    ################################################

    alpha2_ttest = 0.05  # two-sided t-tests: alpha/2

    if len(paths_samples) > 1:
        g_post.plot_vulcano_plot_for_gene_distribution(main_output_dir, fnames_gtc_param, column_names,
                                                       dfs_stat, names_gtc_param_ranks, df_pathway_groups,
                                                       alpha2_ttest_rel=alpha2_ttest, alpha2_ttest_ind=alpha2_ttest)

#################################
    print('... post-processing finished post-processing')
