#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os
import shutil
import gtc.post_proc as g_post


def copy_files_into_same_folder(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list,
    fnames_to_copy: list
) -> None:

    """Link the selected files of the patient samples
    in the same folder with the following structure:
    # -gtc/
    # -Sample_1/
    #  |-Results/
    #    |-file_A
    #    |-file_Z
    # -Sample_N/
    #    |-file_A
    #    |-file_Z
    # -Results_220507_18h49/
    #  |-file_A/
    #    |-Sample_1.lnk
    #    |-Sample_N.lnk
    #  |-file_Z/
    #    |-Sample_1.lnk
    #    |-Sample_N.lnk"""

    out_dirs = [main_output_dir + g_post.rm_ext(fname) + '/' for fname in fnames_to_copy]  # Create the output directory for the link files
    g_post.create_dir(out_dirs)

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)  # name of gtc param file without '.txt', e.g. 'Gtc_Parameters_angio_uni_uni_un50_th160_va010_uni_bly_cly_opy'

    for path_sample in paths_samples:
        sample = g_post.extract_sample_name_from_path(path_sample)
        print('-Back up of fname_to_copy files of sample %s' % sample)

        for name_gtc_param in names_gtc_param:

            for fname_to_copy in fnames_to_copy:  # name of the file to link, e.g. 'Plot_blend_gene combined masks.png'
                path_src = path_sample + 'Results/' + name_gtc_param + '/' + fname_to_copy
                path_dst = main_output_dir + g_post.rm_ext(fname_to_copy) + '/' + \
                           sample + '__' + name_gtc_param + '.' + g_post.get_ext(fname_to_copy)
                # print(path_src); print(path_dst); print(os.path.isfile(path_src)); print('')

                if os.path.isfile(path_src):  # if file exists
                    shutil.copy2(path_src, path_dst)  # copy files
                    # os.link(path_src, path_link)  # create hard link

#################################
