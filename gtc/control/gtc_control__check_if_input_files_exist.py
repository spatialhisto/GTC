#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os


def check_if_input_files_exist(
    p: dict
):

    """Check if the input files defined in gtc parameters exist."""

    for fname in p['files'].values():
        if not os.path.exists(fname):
            raise ValueError("The following input file does not exist: %s "
                             "- Check the file paths' name in 'Gtc-Parameters'!" % fname)

#################################
