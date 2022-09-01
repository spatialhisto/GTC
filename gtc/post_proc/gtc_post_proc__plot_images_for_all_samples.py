#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import math as math
import pandas as pd
import gtc.mask as g_msk
import gtc.post_proc as g_post
import matplotlib.pyplot as plt
from typing import Tuple


def plot_images_for_all_samples(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list,
    dict_disease_history: dict,
    df_overlap: pd.DataFrame,
    fname_image_to_plot: str,
    scale_fac_plot: float = 1.25,
    img_dims_plots: Tuple[int, int] = (500, 500),
    pos_txt_box: Tuple[float, float] = (0.01, 0.98),
    num_rows_per_plot: int = 10,
    font_size_box: int = 10,
    font_size_title: int = 18,
    font_size_ytitle: int = 12,
    pad_title: int = 20,
    pad_label: int = 10,
    save_res: int = 300
) -> None:

    """Plot all sample images
    for all gtc_param cases
    in one plot."""

    DEBUG_ONLY_1_PLOT = False

    ####

    path_out = main_output_dir + 'Summary_' + g_post.rm_ext(fname_image_to_plot) + '/'
    g_post.create_dir(path_out)

    empty_img = g_msk.new_black_color_image(list(img_dims_plots))  # empty black image
    he_images = g_post.import_and_scale_all_he_images(paths_samples, fnames_gtc_param, img_dims_plots)

    names_samples = g_post.extract_sample_name_from_path(paths_samples)
    names_gtc_param = list(df_overlap['name_gtc_param'])

    plot_label_with_overlap_value = 'yes' if 'overlap' in fname_image_to_plot else 'no'

    num_plots = 1 if DEBUG_ONLY_1_PLOT else math.ceil(len(names_gtc_param) / num_rows_per_plot)  # only 1 plot for debugging

    for ii in range(num_plots):
        print('-Creating plot %d of %d' % (ii + 1, num_plots))

        gtc_param_start = ii * num_rows_per_plot
        gtc_param_end = (ii + 1) * num_rows_per_plot

        names_gtc_param_sub = names_gtc_param[gtc_param_start:gtc_param_end]
        len_sub = len(names_gtc_param_sub)

        num_empty = (num_rows_per_plot - len_sub - 1) if len_sub < num_rows_per_plot else 0  # fill up empty rows for last plot sheet to keep format style
        row_names = ['H&E'] + names_gtc_param_sub + ['empty'] * num_empty

        num_rows, num_cols = num_rows_per_plot, len(paths_samples) + 2
        figsize = g_post.calc_figure_size(img_dims_plots, num_rows, num_cols, scale_fac_plot, save_res)

        fig, axs = plt.subplots(len(row_names), len(names_samples), figsize=figsize)  # define subplot

        for ss, name_sample in enumerate(names_samples):  # loop over samples - columns

            for rr, row_name in enumerate(row_names):  # loop over Gtc_Parameters_xxx - rows

                if row_name == 'H&E':
                    img = he_images[name_sample]
                elif row_name == 'empty':
                    img = empty_img
                else:
                    path_img = main_output_dir + g_post.rm_ext(fname_image_to_plot) + '/' + \
                               name_sample + '__' + row_name + '.' + g_post.get_ext(fname_image_to_plot)
                    img = g_post.import_and_scale_image(path_img, img_dims_plots)

                ax = axs[rr, ss]
                ax.imshow(img, extent=[0, img_dims_plots[1], 0, img_dims_plots[0]], aspect='auto',
                          interpolation='none', resample=False, filternorm=False)

                ax.axes.xaxis.set_ticks([])  # turn off ticks and tick labels
                ax.axes.yaxis.set_ticks([])

                if row_name not in ['H&E', 'empty']:  # textbox with number of detected iss genes
                    index = g_post.get_row_index(df_overlap, 'name_gtc_param', row_name)
                    if plot_label_with_overlap_value == 'yes':
                        ax.text(pos_txt_box[0], pos_txt_box[1], 'overlap = %1.3f' % df_overlap[name_sample][index],
                                         transform=ax.transAxes, fontsize=font_size_box, verticalalignment='center',
                                         bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=1.0))

        for ax, name_sample in zip(axs[0], names_samples):  # set column titles
            if dict_disease_history[name_sample] == 'yes':
                ax.set_title(name_sample, color='red', fontsize=font_size_title, pad=pad_title)
            else:
                ax.set_title(name_sample, color='green', fontsize=font_size_title, pad=pad_title)

        for ax, row_name in zip(axs[:, 0], row_names):  # set row titles
            if row_name not in ['H&E', 'empty']:
                index = g_post.get_row_index(df_overlap, 'name_gtc_param', row_name)
                rank = 'rank = %d' % df_overlap['rank'][index]
                geom_mean = 'geometric mean = %1.3f' % df_overlap['geometric_mean'][index]
                row_name = row_name.replace('Gtc_Parameters_', '')  # shorten name
                row_name = rank + '\n\n' + geom_mean + '\n\n' + row_name.rjust(len(max(row_names)))
            ax.set_ylabel(row_name, rotation=0, labelpad=pad_label, fontsize=font_size_ytitle, color='black',
                          horizontalalignment='right', verticalalignment='center')

        plt.subplots_adjust(hspace=0.1, wspace=0.1, bottom=0, top=1, left=0, right=1)  # spacing between subplots
        fig.tight_layout()

        plt.savefig(path_out + 'image' + ('__%02d' % (ii + 1)) + '.png', dpi=save_res)
        plt.close(fig)

#################################
