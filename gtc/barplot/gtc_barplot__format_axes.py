#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.plot as g_plt
import matplotlib.pyplot as plt


def format_axes(
    ax: plt.Axes,
    df_unit_sub: pd.DataFrame,
    unit: str,
    pos_group: np.ndarray,
    txt_ylab: str,
    txt_size: int
) -> plt.Axes:

    """Format the figure axes."""

    ax.set_xlabel('Genes', fontsize=txt_size+1)
    ax.tick_params(axis='x', labelsize=txt_size)
    ax.set_xticks(pos_group)  # ensures one tick per gene, otherwise we get fewer
    ax.set_xticklabels(df_unit_sub['genes'].astype(str).values, rotation=45, rotation_mode='anchor', ha='right')

    ax.set_ylabel(txt_ylab + ' ' + unit, fontsize=txt_size+1)
    ax.tick_params(axis='y', labelsize=txt_size)
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax.yaxis.set_major_formatter(g_plt.sci_notation_format())

    return ax

#################################
