#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.post_proc as g_post


def save_excel_files_for_counts(
    main_output_dir: str,
    fnames_gtc_param: list,
    column_names: list,
    dfs_counts: dict
) -> None:

    """Write the data as multiple
    sheet excel files with:
     - names_gtc_param as file name,
     - column_names as sheet names,
     - genes as rows and
     - names_samples as columns."""

    path_out = main_output_dir + 'Summary_count_matrix/'
    g_post.create_dir(path_out)

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    for name_gtc_param in names_gtc_param:
        fname_excel = path_out + name_gtc_param + '.xlsx'
        excel_file = pd.ExcelWriter(fname_excel, engine='xlsxwriter')

        for column_name in column_names:
            df_save = pd.DataFrame(data=dfs_counts[name_gtc_param][column_name])  # create data frame
            df_save = df_save.sort_values(by='genes')

            sheet_name = column_name.replace('in ', '')  # length of name of sheet must be <31 chars
            sheet_name = sheet_name.replace('tissue ', '')
            sheet_name = sheet_name.replace('neoplastic', 'neo')
            sheet_name = sheet_name.replace('connective in tumor', 'stroma')
            sheet_name = sheet_name.replace(' [-]', '')  # Invalid Excel character '[]:*?/\'
            sheet_name = sheet_name.replace(' [um-2]', '')
            sheet_name = sheet_name.replace("'", '')  # Sheet name cannot start or end with an apostrophe

            if len(sheet_name) > 31:
                raise ValueError("Excel worksheet name must be <= 31 chars:\n"
                                 "Sheetname: '%s' has the length %d" % (sheet_name, len(sheet_name)))

            df_save.to_excel(excel_file, sheet_name=sheet_name, index=False)

        excel_file.save()

#################################
