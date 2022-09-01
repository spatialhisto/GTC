#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import re
import os
import math
import cv2
import numpy as np
import pandas as pd
import gtc.setup as g_set
import gtc.main_fct as g_mfct
import matplotlib.colors as mc
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from typing import Tuple, Union


def quote(
    texts: Union[str, list]
) -> Union[str, list]:

    """Set quotation marks inside
    a single string or a list of
    strings."""

    def q(s):
        return ('\'%s\'' % s)

    if type(texts) == str:
        text_quote = q(texts)
    else:
        text_quote = [q(t) for t in texts]

    return text_quote


####


def get_row_index(
    df: pd.DataFrame,
    col_name: str,
    col_value: str
) -> int:

    """Return the first row index
    of the occurence of the value
    in the column of the data frame.
    This is necessary since pandas
    can change th order of the
    data frame."""

    return df[df[col_name] == col_value].index[0]


####


def rm_ext(
    fnames: Union[str, list]
) -> Union[str, list]:

    """Remove extension from
    file name string or a list
    of file name strings."""

    def rm(s):
        return s.rsplit('.')[0]

    if type(fnames) == str:
        names = rm(fnames)
    else:
        names = [rm(f) for f in fnames]

    return names


####


def get_ext(
    fnames: Union[str, list]
) -> Union[str, list]:

    """Return file extension from
    a single file name string or
    a list of file name strings."""

    def ge(s):
        return s.rsplit('.')[1]

    if type(fnames) == str:
        fnames_ext = ge(fnames)
    else:
        fnames_ext = [ge(f) for f in fnames]

    return fnames_ext


####


def create_dir(
    fnames: Union[str, list]
) -> None:

    """Create single or
    multiple folders."""

    if type(fnames) == str:
        fnames = [fnames]

    for fname in fnames:
        Path(fname).mkdir(parents=True, exist_ok=True)


####


def extract_sample_name_from_path(
    paths_samples: Union[str, list]
) -> Union[str, list]:

    """Extract the sample name from the
    sample path or the sample names from
    a list of sample paths, e.g. 'exp42_121KS'."""

    def extract(s):
        return s.split('/')[-2]

    if type(paths_samples) == str:
        sample_names = extract(paths_samples)
    else:
        sample_names = [extract(p) for p in paths_samples]

    return sample_names


####


def assemble_path_main_output_dir(
    path_project: str
) -> str:

    """Assemble the path to main
    output folder."""

    now = datetime.now()  # current date and time
    year = now.strftime('%y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime('%H')
    minute = now.strftime('%M')

    fname = path_project + 'Results_' + year + month + day + '_' + hour + 'h' + minute + '/'

    return fname


####


def create_dict_disease_history(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list,
    DEBUG: bool
) -> dict:

    """Read out the information if the
    patient sample is/is not from a relaps
    case from the Gtc_Parameterts.txt file.
    In debugging modus, the file names are
    loaded from the Backup_Gtc_Parameters
    folder files."""

    dict_disease_history = dict()

    for path_sample in paths_samples:
        sample = extract_sample_name_from_path(path_sample)

        if not DEBUG:
            fname_gtc_param = path_sample + fnames_gtc_param[0]
        else:
            fname_gtc_param = main_output_dir + 'Backup_Gtc_Parameters/' + sample + '__Gtc_Parameters.txt'

        p = g_set.read_gtc_parameter_settings(fname_gtc_param)

        dict_disease_history[sample] = p['disease_history_relaps']

    return dict_disease_history


####


def extract_float_from_string(
    txt: str,
    substring_start: str,
    substring_end: str
) -> float:

    """Extract a float number from a text.
    The number is between substring_start
    and substring_end."""

    pos_substr_start = txt.find(substring_start)  # find start position and end position of substring
    pos_substr_end = txt.find(substring_end)

    substring = txt[pos_substr_start:pos_substr_end]  # extract substring from string
    number_str = re.findall('\d+\.\d+', substring)  # find all float numbers in substring as list
    number = float(number_str[0])  # convert str to float

    return number


####


def create_dict_names_gtc_param_ranks(
    df_overlap: pd.DataFrame
) -> dict:

    """Assign the rank of the gene
    mask overlap with the drawn mask
    to the name_gtc_param."""

    names_gtc_param_ranks = dict()

    for _, row in df_overlap.iterrows():
        rank = row['rank']
        name_gtc_param = row['name_gtc_param']
        names_gtc_param_ranks[name_gtc_param] = '%03d' % rank  # as string

    return names_gtc_param_ranks


####


def calc_figure_size(
    img_dims_plot: Tuple[int, int],
    num_rows: int,
    num_cols: int,
    scale_fac_plot: float,
    save_res: int,
) -> Tuple[float, float]:

    """Calculate the dimension of the
    subplot to keep the dimension of
    the images as specified in
    img_dims_plot."""

    fac = scale_fac_plot / save_res

    width = fac * num_cols * img_dims_plot[0]
    height = fac * num_rows * img_dims_plot[1]

    figsize = width, height

    return figsize


####


def import_and_scale_image(
    path_image: str,
    new_dims: Tuple[int, int]
) -> np.ndarray:

    """Import a image and scale it
    to new dimensions."""

    if (os.path.exists(path_image) and
        os.path.isfile(path_image) and
        path_image.endswith('.png')):

        image = cv2.imread(path_image)
        image = cv2.resize(image, (new_dims[1], new_dims[0]), interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    else:
        raise ValueError('Cannot import image!\nCheck path: %s' % path_image)

    return image


####


def import_and_scale_all_he_images(
    paths_samples: list,
    fnames_gtc_param: list,
    new_dims: Tuple[int, int]
) -> dict:

    """Import all necessary H&E images
    and scale them to new dimensions."""

    he_images = dict()

    for path_sample in paths_samples:
        name_sample = extract_sample_name_from_path(path_sample)
        name_gtc_param = rm_ext(fnames_gtc_param[0])

        path_image = path_sample + 'Results/' + name_gtc_param + '/Plot_mask_or_img_virtual H&E image.png'
        image = import_and_scale_image(path_image, new_dims)
        he_images[name_sample] = image

    return he_images


####


def limit_number_of_fnames_gtc_param(
    df_overlap: dict,
    num_top_ranks: int
) -> list:

    """Limit the number of fnames_gtc_param
    for the further post-processing."""

    names_gtc_param = df_overlap[df_overlap['rank'] <= num_top_ranks]['name_gtc_param']

    fnames_gtc_param_new = [name_gtc_param + '.txt' for name_gtc_param in list(names_gtc_param)]

    return fnames_gtc_param_new


####


def split_column_names_in_mask_types_and_tissues_and_units(
    column_names: list
) -> Tuple[list, list, list]:

    """Split the column name in its unique parts:
     - pre_mask_types, e.g, ['Counts in drawn tissue ', 'Counts in gene tissue ']
     - tissues, e.g. ['neoplastic', 'non-neoplastic']
     - units, e.g. [' [-]', ' per area [um-2]', ' per cell [-]']"""

    col_name_parts = [col.split("'") for col in column_names if col != 'Genes']
    col_name_parts = np.array(col_name_parts)

    pre_mask_types = list(np.unique(col_name_parts[:, 0]))

    tissues = list(np.unique(col_name_parts[:, 1]))
    tissues = quote(tissues)

    units = list(np.unique(col_name_parts[:, 2]))

    return pre_mask_types, tissues, units


####


def analyze_structure_count_matrix_files(
    main_output_dir: str
) -> Tuple[list, list]:

    """Analyze the structure of the files
    'Count_matrix.csv' and extract:
     - genes
     - column name prefixes and mask types
     - column name tissues
     - column name units."""

    path_dir = main_output_dir + 'Count_matrix' + '/'
    path_files = [path_dir + file for file in os.listdir(path_dir) if file.endswith(".csv")]

    df = pd.read_csv(path_files[0], delimiter=";")  # all Count_matrix.csv files have same structure, open arbitrary file

    df.columns = ['Genes' if col_name == 'Unnamed: 0' else col_name for col_name in list(df.columns)]  # rename first column
    column_names = list(df.columns)
    column_names.remove('Genes')  # read out column names

    genes = [gene for gene in list(df['Genes']) if gene != 'cells']  # read out genes

    return genes, column_names


####


def build_data_in_dict(
    main_output_dir: str,
    names_samples: list,
    names_gtc_param: list
) -> dict:

    """Build a dictionary with the
    following structure for the data
    input from the csv count files:
    d_in[name_sample] = csv_data_frame"""

    names = [s + '__' + g for s in names_samples for g in names_gtc_param]  # e.g., exp42_121KS__Gtc_Parameters

    d = dict()
    for name in names:
        path_file = main_output_dir + 'Count_matrix/' + name + '.csv'
        df = pd.read_csv(path_file, delimiter=";", decimal=",")
        df.columns = ['genes' if column_name == 'Unnamed: 0' else column_name for column_name in list(df.columns)]  # rename first column
        d[name] = df

    return d


####


def build_data_out_dict(
    names_gtc_param: list,
    column_names: list
) -> dict:

    """Build a dictionary with the following
    structure for the data output:
    d_out[name_gtc_param][column_name] = None"""

    d = {name_gtc_param: {} for name_gtc_param in names_gtc_param}
    for name_gtc_param in names_gtc_param:
        for column_name in column_names:
            d[name_gtc_param][column_name] = None

    return d


####


def build_stat_test_dict(
    names_gtc_param: list,
    pre_mask_types: list,
    units: list
) -> dict:

    """Build a dictionary with the following
    structure for the statistical testing:
    d_stat[name_gtc_param][pre_mask_type + unit] = None"""

    d = {name_gtc_param: {} for name_gtc_param in names_gtc_param}
    for name_gtc_param in names_gtc_param:
        for pre_mask_type in pre_mask_types:
            for unit in units:
                d[name_gtc_param][pre_mask_type + unit] = None

    return d


####


def extend_discrete_tab10_cmap(
    num_colors: int,
    num_subcolors: int,
    continuous: bool = False
) -> mc.ListedColormap:

    """Create individual colors based on the tab10-color map
    where num_colors defines the main colors and num_subcolors
    the number of colors derived therefrom.
    Example for use:
        n_col = 4; n_scol = 3; tot_col = (n_col * n_scol)
        c1 = categorical_cmap(n_col, n_scol)
        plt.scatter(np.arange(tot_col), np.ones(tot_col)+1, c=np.arange(tot_col), s=180, cmap=c1)"""

    if num_colors > plt.get_cmap('tab10').N:
        raise ValueError('The tab10-colormap has only 10 colors - decrease num_colors to max 10.')

    if continuous:
        ccolors = plt.get_cmap('tab10')(np.linspace(0, 1, num_colors))
    else:
        ccolors = plt.get_cmap('tab10')(np.arange(num_colors, dtype=int))

    cols = np.zeros((num_colors * num_subcolors, 3))

    for ii, c in enumerate(ccolors):
        chsv = mc.rgb_to_hsv(c[:3])

        arhsv = np.tile(chsv, num_subcolors).reshape(num_subcolors, 3)
        arhsv[:, 1] = np.linspace(chsv[1], 0.25, num_subcolors)
        arhsv[:, 2] = np.linspace(chsv[2], 1.00, num_subcolors)

        rgb = mc.hsv_to_rgb(arhsv)

        cols[ii*num_subcolors:(ii+1)*num_subcolors, :] = rgb

    cmap_ext = mc.ListedColormap(cols)

    return cmap_ext


####


def discrete_colors_from_continuous_cmap(
    num_colors: int,
    cmap: str = 'jet'
) -> mc.ListedColormap:

    """Derive discrete color map
    from continuous color map"""

    cmap_dis = plt.cm.get_cmap(cmap, num_colors)

    return cmap_dis


####


def add_color_grey_to_cmap_list(
    cmap: mc.ListedColormap
) -> list:

    """Add color to
    discrete color map."""

    color_to_add = [(0.5, 0.5, 0.5, 1.0)]  # rgba color

    ###

    cmap_list = [cmap(i) for i in range(cmap.N)]

    cmap_list = color_to_add + cmap_list

    return cmap_list


####


def calc_miss_df_values_for_vulcano_plot(
    df: pd.DataFrame,
    df_pathway_groups: pd.DataFrame,
    test_type: str,
    alpha2_ttest: float,
    k: float = -1.0,
    d: float = 5.0,
    alpha_opacity: float = 0.4
) -> pd.DataFrame:

    """Set the point color and
    opacity depending on the
    position of the position
    on the vulcano plot."""

    symbols = ['o', '^', 's', 'd', 'X']  # 'o' is for insignificant genes

    ###

    def test_significance(y):
        is_significant = 'yes' if (y >= thresh_pvalue) else 'no'
        return is_significant

    def test_label(x, y, is_significant):  # test if gene gets a label in the vulcano plot
        if test_type == 'ttest_rel':
            if x >= 0:
                is_labeled = 'yes' if (y >= k * x + d) else 'no'  # does gene lie over kx+d line
            else:
                is_labeled = 'yes'
        else:
            is_labeled = 'yes'
        is_labeled = 'yes' if (is_labeled == 'yes' and is_significant == 'yes') else 'no'
        return is_labeled

    def set_symbol(code_number):
        if code_number == 0:
            symbol_number = 0  # 'o' is for insignificant genes
        else:
            symbol_number = ((code_number - 1) % (len(symbols) - 1)) + 1
        symbol = symbols[int(symbol_number)]
        return symbol

    def set_rgba_color(code_number):
        if code_number == 0:
            color_number = 0  # grey (cmap_list[0]) is for insignificant genes
        else:
            color_number = ((code_number - 1) // (len(symbols) - 1)) + 1
        rgba_color = list(cmap_list[int(color_number)])
        return rgba_color

    def set_opacity_color(is_labeled, rgba_color):
        alpha_color = 1.0 if (is_labeled == 'yes') else alpha_opacity  # opacity on vulcano plot
        alpha_color = rgba_color[3] * alpha_color  # change total opacity of color point
        return alpha_color

    ###

    thresh_pvalue = - math.log10(alpha2_ttest)  # threshold value for significance of ttest

    df = pd.merge(df, df_pathway_groups, how='left', on='genes')  # combine data frames

    df['log2_fold_changes'] = np.log2(df['mean1'] / df['mean2'])  # calculate x-values
    df['log10_pvalues'] = - np.log10(df['pvalues'])  # calculate y-values

    df['is_significant'] = df.apply(lambda x: test_significance(x['log10_pvalues']), axis=1)  # is gene significant?
    df['is_labeled'] = df.apply(lambda x: test_label(x['log2_fold_changes'], x['log10_pvalues'], x['is_significant']), axis=1)  # is gene labeled?

    df = df.sort_values(by=['group_names'])

    df['code_numbers'] = (df[df["is_significant"] == 'yes']).groupby(['group_names']).ngroup()
    df['code_numbers'] = df['code_numbers'] + 1
    df['code_numbers'] = df['code_numbers'].fillna(0)

    num_colors = math.ceil(max(df['code_numbers'] / (len(symbols) - 1)))  # number of symbols for significant genes
    cmap = extend_discrete_tab10_cmap(num_colors, 1)
    cmap_list = add_color_grey_to_cmap_list(cmap)  # create color map

    df['symbols'] = df.apply(lambda x: set_symbol(x['code_numbers']), axis=1)  # assign symbols to genes
    df['rgba_colors'] = df.apply(lambda x: set_rgba_color(x['code_numbers']), axis=1)  # assign color to genes
    df['alphas_opacity'] = df.apply(lambda x: set_opacity_color(x['is_labeled'], x['rgba_colors']), axis=1)  # assign opacity to genes

    return df

#################################
