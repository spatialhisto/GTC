#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np


def create_tissue_non_neoplastic_mask(
    masks: dict
) -> np.ndarray:

    """Create a mask for the non-neoplastic tissues as disjoint
    of the masks composite, neoplastic and connective in tumor."""

    mask_tissues = masks["gene tissue 'neoplastic'"]

    mask = cv2.subtract(masks["gene tissue 'composite'"], mask_tissues)  # tissue_neoplastic = tissue_composite - (tissue_neoplastic + tissue_stroma), results limited between 0 and 255 due to saturate

    return mask

#################################
