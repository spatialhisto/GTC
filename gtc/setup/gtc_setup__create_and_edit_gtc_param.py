#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import gtc.setup as g_set
import gtc.control as g_ctrl


def create_and_edit_gtc_param(
    fname_gtc_param: str
) -> dict:

    """Load gtc parameter file, build parameter
    dictionary, setup input and output paths,
    check if input files exist and scale the
    gtc parameters by img_scale_factor."""

    p = g_set.read_gtc_parameter_settings(fname_gtc_param)  # load gtc parameters
    print('Path of used gtc parameter file: %s' % fname_gtc_param)
    print('The original gtc parameters dictionary entries: %s' % p)

    ####

    p['input'] = g_set.assemble_input_dirname(fname_gtc_param)  # assemble name of input and output folders
    p['output'] = g_set.assemble_output_dirname(fname_gtc_param)

    ####

    p = g_set.scale_gtc_parameters_by_factor(p)  # scale the gtc parameters by img_scale_factor

    ####

    p['img_res_in_dpi'] = 300  # resolution of matplotlib plots

    #####

    p['rgb_colors_drawn_masks'] = {}  # set rgb tissue colors of drawn mask
    p['rgb_colors_drawn_masks'] = {'neoplastic': [196, 47, 26],  # rgb color for red
                                   'non-neoplastic': [144, 194, 38],  # rgb color for green
                                   'connective in tumor': [230, 185, 30]}  # rgb color for yellow

    #####

    g_ctrl.check_if_input_files_exist(p)

    return p

#################################
