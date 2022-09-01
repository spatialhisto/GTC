#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.post_proc as g_post
from scipy import stats


def summarize_overlaps_neoplastic_masks(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list
) -> pd.DataFrame:

    """Build a data frame containing the mask
    overlaps from the Report.txt files and save
    the results as csv file:.
    Rows: names_gtc_param, e.g. Gtc_Parameters_xxx
    Columns: names_samples, e.g. exp42_121KS."""

    names_samples = g_post.extract_sample_name_from_path(paths_samples)
    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    data_dict = {'name_gtc_param': names_gtc_param}   # column with Gtc_Parameters_xxx names

    for name_sample in names_samples:
        data_dict[name_sample] = []  # start new column

        for name_gtc_param in names_gtc_param:
            path_file = main_output_dir + 'Report/' + name_sample + '__' + name_gtc_param + '.txt'

            with open(path_file, 'r') as file:
                txt = file.read().replace('\n', '')  # read text from file as single string

                overlap = g_post.extract_float_from_string(txt, 'has overlap of:', '*** Plot masks')  # extract overlap as float number from text
                data_dict[name_sample].append(overlap)

    df = pd.DataFrame(data=data_dict)  # create data frame

    geometric_mean = list(stats.gmean(df.iloc[:, 1:len(df.columns)], axis=1))  # calculate the geometric average for each row
    df.insert(loc=0, column='geometric_mean', value=geometric_mean)
    df['geometric_mean'] = df['geometric_mean'].round(decimals=3)
    df = df.sort_values(by=['geometric_mean'], ascending=False)

    df.insert(loc=0, column='rank', value=range(1, len(df.index)+1))
    df = df.reset_index(drop=True)

    return df

#################################
