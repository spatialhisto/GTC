#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import matplotlib.pyplot as plt


def format_title_and_legend(
    axs: plt.Axes,
    num_subplots: int,
    txt_tit: str
):

    """Format the figure title."""

    if num_subplots == 1:
        # axs[0, 0].legend(frameon=False, loc='best', fancybox=True)
        axs[0, 0].legend(loc='center left', bbox_to_anchor=(1.15, 0.5), frameon=False, fancybox=True)
        plt.suptitle(txt_tit, fontsize=16, x=0.5, y=0.90)
    else:
        axs[0, 0].legend(loc='upper center', bbox_to_anchor=[0.5, 1.4], frameon=False, fancybox=True, ncol=2)
        plt.suptitle(txt_tit, fontsize=16, x=0.5, y=0.98)

#################################
