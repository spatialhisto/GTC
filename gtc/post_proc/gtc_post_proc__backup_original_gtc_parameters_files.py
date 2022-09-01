#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os
import shutil
import gtc.post_proc as g_post


def backup_original_gtc_parameters_files(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list
) -> None:

    """Backup the original Gtc_Parameters_xxx
     files in the post processing folder."""

    out_dir = main_output_dir + 'Backup_Gtc_Parameters/'
    g_post.create_dir(out_dir)

    for path_sample in paths_samples:
        sample = g_post.extract_sample_name_from_path(path_sample)
        print('-Back up of Gtc_Parameters_xxx files of sample %s' % sample)

        for fname_gtc_param in fnames_gtc_param:
            name_gtc_param = g_post.rm_ext(fname_gtc_param)

            path_src = path_sample + fname_gtc_param
            path_dst = out_dir + sample + '__' + name_gtc_param + '.txt'
            # print(path_src); print(path_dst); print(os.path.isfile(path_src)); print('')

            if os.path.isfile(path_src):  # if file exists
                shutil.copy2(path_src, path_dst)  # copy files
                # os.link(path_src, path_link)  # create hard link

#################################
