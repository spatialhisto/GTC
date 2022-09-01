#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os
import shutil
from pathlib import Path


def assemble_sample_paths(
    path_project: str,
    patient_samples: list
) -> list:

    """Assemble the path of the samples."""

    paths_samples = [path_project + samples for samples in patient_samples]

    return paths_samples


####


def remove_old_results(
    paths_samples: list
) -> None:

    """Remove old results and
    Gtc_Parameters.txt files."""

    remove_old_results_from_samples_dirs(paths_samples)
    remove_old_gtc_param_files_from_samples_dirs(paths_samples)


####


def remove_old_results_from_samples_dirs(
    paths_samples: list
) -> None:

    """Remove previous calculated results
    from the sample paths."""

    paths_results = [path_sample + 'Results/' for path_sample in paths_samples]

    for path_result in paths_results:
        if os.path.isdir(path_result):
            shutil.rmtree(path_result)  # delete directory sample/Results/

            Path(path_result).mkdir(parents=True, exist_ok=True)  # create directory sample/Results/


####


def remove_old_gtc_param_files_from_samples_dirs(
    paths_samples: list
) -> None:

    """Remove Gtc_Parameters_xxx.txt files
    from the sample paths except the
    Gtc_Parameters.txt file."""

    for path_sample in paths_samples:
        objects_in_sample_dir = os.listdir(path_sample)
        fnames_gtc_param = [o for o in objects_in_sample_dir if o.endswith('.txt')]

        fnames_gtc_param.remove('Gtc_Parameters.txt')

        for fname_gtc_param in fnames_gtc_param:
            path_gtc_param = path_sample + fname_gtc_param
            if os.path.exists(path_gtc_param):
                os.remove(path_gtc_param)
                # print('Removed %s' % path_gtc_param)



#################################
