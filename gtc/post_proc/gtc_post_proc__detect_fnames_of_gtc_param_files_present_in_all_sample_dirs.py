#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os


def detect_fnames_of_gtc_param_files_present_in_all_sample_dirs(
    main_output_dir: str,
    paths_samples: list,
    DEBUG: bool
) -> list:

    """Detect the file names of the Gtc_Parameters.txt files
    which are present in all sample directories.
    In debugging modus, the file names are loaded
    from the Backup_Gtc_Parameters folder files."""

    fnames_present_in_all_dirs = list()

    if not DEBUG:
        for ii, path_sample in enumerate(paths_samples):
            objects_in_sample_dir = os.listdir(path_sample)
            fnames_gtc_param = [o for o in objects_in_sample_dir if o.endswith('.txt')]  # Gtc_Parameters.txt files

            if ii == 0:
                fnames_present_in_all_dirs = fnames_gtc_param
            else:
                fnames_present_in_all_dirs = list(set(fnames_gtc_param) & set(fnames_present_in_all_dirs))
    else:
        dir = main_output_dir + 'Backup_Gtc_Parameters/'
        objects_in_sample_dir = os.listdir(dir)

        fnames_present_in_all_dirs = [o.split('__')[-1] for o in objects_in_sample_dir if o.endswith('.txt')]
        fnames_present_in_all_dirs = list(set(fnames_present_in_all_dirs))  # make list unique

    fnames_present_in_all_dirs.sort()  # sort alphabetically

    return fnames_present_in_all_dirs

#################################
