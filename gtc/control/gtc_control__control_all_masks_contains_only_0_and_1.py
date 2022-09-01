#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np


def control_all_masks_contains_only_0_and_1(
    masks: dict,
    c: dict
):

    """Control the binary nature of the masks - only 0 and 255 values."""

    mask_names = ['gene ' + mask_name for mask_name in c['tissue_mask_names_calc']]

    for mask_name in mask_names:
        not_ok = np.any(np.logical_not(np.logical_or(masks[mask_name] == 0, masks[mask_name] == 255)))

        print('-Check %s is %s' % (mask_name, 'not ok' if not_ok is True else 'ok'))

    mask_names = ['drawn ' + mask_name for mask_name in c['tissue_mask_names_calc']]

    for mask_name in mask_names:
        not_ok = np.any(np.logical_not(np.logical_or(masks[mask_name] == 0, masks[mask_name] == 255)))

        print('-Check %s is %s' % (mask_name, 'not ok' if not_ok is True else 'ok'))

#################################
