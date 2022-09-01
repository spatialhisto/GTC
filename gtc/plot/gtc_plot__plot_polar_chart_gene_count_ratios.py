#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple
from math import pi


def plot_polar_chart_gene_count_ratios(
    df_counts: pd.DataFrame,
    p: dict,
    DEBUG: bool,
    fontsize: str = 'small',
    plot_size: Tuple[float, float] = (4.0, 4.0),  # (width, height) subplot size
    save_res: int = 300
) -> None:

    """Plot ratios of gene counts in gene-based
    and drawn mask for tissues."""

    gene_names = df_counts['genes']
    num_genes = len(gene_names)
    theta_genes = 2 * pi / num_genes * np.arange(num_genes)  # radiant position of genes

    gene_names.append(pd.Series(gene_names[0]))
    theta_genes = np.append(theta_genes, 0)  # close line start-stop

    tissues = ["'neoplastic'", "'non-neoplastic'"] if DEBUG else ["'neoplastic'"]
    colors = ['orangered', 'limegreen'] if DEBUG else ['orangered']
    y_lim_max = 2.5 if DEBUG else 2.0

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=plot_size)

    for tissue, color in zip(tissues, colors):
        col_name_gene = 'Counts in gene tissue ' + tissue + ' per cell [-]'
        col_name_drawn = 'Counts in drawn tissue ' + tissue + ' per cell [-]'

        ratios = df_counts[col_name_gene] / df_counts[col_name_drawn]
        ratios = ratios.fillna(1.0)  # set NaN values from divisioin through zero to 1
        ratios = np.where(ratios > y_lim_max, y_lim_max, ratios)  # limit the ratio values to maximum value
        ratios = np.append(ratios, ratios[0])  # close line start-stop

        ax.plot(theta_genes, ratios, c=color, label=tissue)

    ax.set_xticklabels([])
    ax.set_ylim([0, y_lim_max])  # limit the values

    if DEBUG:
        ax.legend(loc="best", frameon=False, fontsize=fontsize, bbox_to_anchor=(1.1, 1.08))

    fig.tight_layout()
    plt.savefig(p['output'] + 'Plot_polar_chart_gene_count_ratios.png', dpi=save_res)
    plt.close('all')

#################################
