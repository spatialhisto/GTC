#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np


def calc_overlap_neoplastic_tissue_in_drawn_and_gene_build_masks(
    masks: dict,
) -> float:

    """Count ratio of overlap for the neoplastic
    tissues in the masks A (ground truth) and B
    (mask to test) by:
    overlap = counts[A and B]^2 / (counts[A] * counts[B]).
    The vales of overlap lie between [0, 1]."""

    A = masks["drawn tissue 'neoplastic'"] == 255
    B = masks["gene tissue 'neoplastic'"] == 255

    A_and_B = np.sum(np.logical_and(A, B))

    if np.sum(A) > 0 and np.sum(B) > 0:
        overlap = float(A_and_B) ** 2 / (float(np.sum(A)) * float(np.sum(B)))
    else:
        overlap = 0

    return overlap

#################################
