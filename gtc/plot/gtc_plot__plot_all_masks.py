#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import gtc.plot as g_plt


def plot_all_masks(
    orig_img_props: dict,
    masks: dict,
    p: dict,
    DEBUG: bool
):

    """Save a small version of each mask as png-file."""

    if not DEBUG:
        mask_names = ["gene combined masks",
                      "drawn combined masks",
                      "overlap tissue 'neoplastic' masks",
                      "virtual H&E image"]

        for mask_name in mask_names:
            g_plt.save_resized_image(orig_img_props, masks[mask_name], 'Plot_mask_or_img_' + mask_name, p)

    else:
        for mask_name in masks.keys():
            print('-Plot mask or image for %s' % mask_name)

            g_plt.save_resized_image(orig_img_props, masks[mask_name],  'Plot_mask_or_img_' + mask_name, p)

#################################
