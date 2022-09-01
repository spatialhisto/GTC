#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.post_proc as g_post
import matplotlib.pyplot as plt
from typing import Tuple


def plot_images_for_all_samples_for_single_gtc_param(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list,
    dict_disease_history: dict,
    df_overlap: pd.DataFrame,
    fnames_images: str,
    scale_fac_plot: float = 1.25,
    img_dims_plots: Tuple[int, int] = (2000, 2000),
    pos_txt_box: Tuple[float, float] = (0.01, 0.98),
    font_size_box: int = 30,
    font_size_title: int = 40,
    pad_title: int = 20,
    pad_label: int = 10,
    save_res: int = 300
) -> None:

    """Plot all images from
    fnames_to_copy in one plot
    if only one gtc_param
    file exists."""

    names_gtc_param = list(df_overlap['name_gtc_param'])

    if len(names_gtc_param) == 1:
        name_gtc_param = names_gtc_param[0]
        names_samples = g_post.extract_sample_name_from_path(paths_samples)
        fnames_images_with_he = ['H&E'] + fnames_images

        he_images = g_post.import_and_scale_all_he_images(paths_samples, fnames_gtc_param, img_dims_plots)  # import H&E

        num_rows, num_cols = len(fnames_images_with_he), len(paths_samples)
        figsize = g_post.calc_figure_size(img_dims_plots, num_rows, num_cols, scale_fac_plot, save_res)

        fig, axs = plt.subplots(len(fnames_images_with_he), len(names_samples), figsize=figsize)  # define subplot

        for rr, fname in enumerate(fnames_images_with_he):  # loop over Gtc_Parameters_xxx - rows

            plot_label_with_overlap_value = 'yes' if 'overlap' in fname else 'no'

            for ss, name_sample in enumerate(names_samples):  # loop over samples - columns

                if fname == 'H&E':
                    img = he_images[name_sample]
                else:
                    path_img = main_output_dir + g_post.rm_ext(fname) + '/' + \
                               name_sample + '__' + name_gtc_param + '.' + g_post.get_ext(fname)
                    img = g_post.import_and_scale_image(path_img, img_dims_plots)

                ax = axs[rr, ss]
                ax.imshow(img, extent=[0, img_dims_plots[1], 0, img_dims_plots[0]])

                ax.axes.xaxis.set_ticks([])  # turn off ticks and tick labels
                ax.axes.yaxis.set_ticks([])

                index = g_post.get_row_index(df_overlap, 'name_gtc_param', name_gtc_param)
                if plot_label_with_overlap_value == 'yes':
                    ax.text(pos_txt_box[0], pos_txt_box[1], 'overlap = %1.3f' % df_overlap[name_sample][index],
                                     transform=ax.transAxes, fontsize=font_size_box, verticalalignment='center',
                                     bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=1.0))

        for ax, name_sample in zip(axs[0], names_samples):  # set column titles
            if dict_disease_history[name_sample] == 'yes':
                ax.set_title(name_sample, color='red', fontsize=font_size_title, pad=pad_title)
            else:
                ax.set_title(name_sample, color='green', fontsize=font_size_title, pad=pad_title)

        for ax, row_name in zip(axs[:, 0], fnames_images_with_he):  # set row titles
            ax.set_ylabel('', rotation=0, labelpad=pad_label, size='large', color='black',
                          horizontalalignment='right', verticalalignment='center')

        plt.subplots_adjust(hspace=0.1, wspace=0.1, bottom=0, top=1, left=0, right=1)  # spacing between subplots
        fig.tight_layout()

        plt.savefig(main_output_dir + 'Summary_all_images.png', dpi=save_res)
        plt.close(fig)

#################################
