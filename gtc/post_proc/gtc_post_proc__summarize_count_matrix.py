#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.post_proc as g_post


def summarize_count_matrix(
    main_output_dir: str,
    paths_samples: list,
    fnames_gtc_param: list,
    genes: list,
    column_names: list
) -> dict:

    """Build a data frame containing the mask
    overlaps from the Report.txt files.
    Rows: genes, e.g. 'MET'
    Columns: names_samples, e.g. exp42_121KS."""

    names_samples = g_post.extract_sample_name_from_path(paths_samples)
    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    data_in = g_post.build_data_in_dict(main_output_dir, names_samples, names_gtc_param)
    data_out = g_post.build_data_out_dict(names_gtc_param, column_names)

    for name_gtc_param in names_gtc_param:
        print('-Summary for %s' % name_gtc_param)

        for column_name in column_names:
            df = pd.DataFrame(np.nan,
                              index=range(0, len(genes)),
                              columns=['genes'])
            df['genes'] = genes

            for gene in genes:
                for name_sample in names_samples:
                    name_csv_file = name_sample + '__' + name_gtc_param

                    index = g_post.get_row_index(data_in[name_csv_file], 'genes', gene)
                    count_value = data_in[name_csv_file][column_name][index]

                    index = g_post.get_row_index(df, 'genes', gene)
                    df.at[index, name_sample] = count_value

            if df.isnull().values.any():
                raise ValueError('Data frame contains NaNs!\nCheck %s and %s' % (name_gtc_param, column_name))

            data_out[name_gtc_param][column_name] = df

    return data_out

#################################
