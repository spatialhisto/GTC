#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import matplotlib.pyplot as plt


def calc_fig_dims(
    df: pd.DataFrame,
    p: dict,
) -> (plt.Figure, plt.Axes, int, int, int):

    """Calculate the figure subplot properties."""

    num_genes_per_subplot = p['barplot_props']['num_genes_per_subplot']

    ####

    num_genes = len(df['genes'])  # number of genes
    num_subplots = num_genes // num_genes_per_subplot + (0 if num_genes % num_genes_per_subplot == 0 else 1)

    size_subplots = {'x': p['barplot_props']['size_subplot']['x'],
                     'y': p['barplot_props']['size_subplot']['y']}

    fig, axs = plt.subplots(num_subplots, 1, facecolor='w', edgecolor='k', squeeze=False,
                            figsize=(size_subplots['x'] * num_genes_per_subplot,
                                     size_subplots['y'] * num_subplots + (1.0 if num_subplots == 1 else 0.0)))

    return fig, axs, num_genes, num_genes_per_subplot, num_subplots

#################################
