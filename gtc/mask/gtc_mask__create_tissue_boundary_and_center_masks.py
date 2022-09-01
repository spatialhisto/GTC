#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import gtc.mask as g_msk


def create_tissue_boundary_and_center_masks(
    masks: dict,
    mask_type: str,
    c: dict,
    p: dict,
    max_disk_radius: int = 101
):

    """Create masks for the center and the boundary of a defined tissue."""

    erosion_size = p['tissue_region_masks']['boundary_size']

    ####

    for mask_name in c['tissue_region_masks_dict'].keys():
        mask_type_name = mask_type + ' ' + mask_name
        print('-Create region mask for %s' % mask_type_name)

        mask_name_center = mask_type + ' ' + c['tissue_region_masks_dict'][mask_name]['center']  # name tissue center mask
        mask_name_boundary = mask_type + ' ' + c['tissue_region_masks_dict'][mask_name]['boundary']  # name tissue boundary mask

        masks[mask_name_center] = g_msk.erode_mask_by_size(masks[mask_type_name], erosion_size, max_disk_radius)  # tissue_center

        masks[mask_name_boundary] = cv2.subtract(masks[mask_type_name], masks[mask_name_center])  # tissue_boundary = tissue_mask - tissue_center, results limited between 0 and 255 due to saturate

#################################
