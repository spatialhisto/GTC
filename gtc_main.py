#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################
#
# GTC - Genes To Count
#

import os
import sys
import gtc.main_fct as g_mfct
import gtc.post_proc as g_post
from multiprocessing import cpu_count, Pool
from functools import partial


if __name__ == "__main__":

    REMOVE_OLD_RESULTS = False

    ############################
    # DEFINE SAMPLES DIRECTORIES
    ############################

    # path_project = 'C:/Users/xxx/'
    path_project = 'C:/Users/o_grubermi/LW_RUN/Tumor_Counts/gtc/data/'

    sample_folders = ['sample_A/', 'sample_B/']
    path_df_pathways_csv = path_project + 'pathways.csv'

    ################
    # PRE-PROCESSING
    ################

    paths_samples = g_mfct.assemble_sample_paths(path_project, sample_folders)

    if REMOVE_OLD_RESULTS:
        g_mfct.remove_old_results(paths_samples)

    ######
    # MAIN
    ######

    for path_sample in paths_samples:
        fnames_gtc_param = [path_sample + file for file in os.listdir(path_sample) if file.endswith(".txt")]  # multiple Gtc_Parameters in project folder

        if len(fnames_gtc_param) != 0:
            g_mfct.main_function(fnames_gtc_param.pop(0))  # call 1st time not in parallel to load original images from net and shrink it

        if len(fnames_gtc_param) != 0:  # if list is not empty after 1st call
            pool = Pool(cpu_count() - 1)

            main_fct = partial(g_mfct.main_function)  # only single argument can be iterated with pool.map function, partial fixes DEBUG
            pool.map(main_fct, fnames_gtc_param)  # call in parallel

    #################
    # POST-PROCESSING
    #################

    main_output_dir = g_post.assemble_path_main_output_dir(path_project)  # create path to main output folder for post-processing results (with time stamp)
    g_post.create_dir(main_output_dir)

    g_post.perform_post_processing(main_output_dir, paths_samples, path_df_pathways_csv)

    #####

    print('... finished')
    sys.exit(0)

#################################
