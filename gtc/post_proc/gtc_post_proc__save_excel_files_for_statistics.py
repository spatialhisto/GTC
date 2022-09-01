#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.post_proc as g_post


def save_excel_files_for_statistics(
    main_output_dir: str,
    fnames_gtc_param: list,
    column_names: list,
    dfs_stat: dict
) -> None:

    """Write the data as multiple
    sheet excel files with:
     - names_gtc_param as file name,
     - column_names as sheet names,
     - genes as rows and
     - names_samples as columns."""

    path_out = main_output_dir + 'Summary_statistics/'
    g_post.create_dir(path_out)

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    pre_mask_types, tissues, units = g_post.split_column_names_in_mask_types_and_tissues_and_units(column_names)

    for name_gtc_param in names_gtc_param:
        fname_excel = path_out + name_gtc_param + '.xlsx'
        excel_file = pd.ExcelWriter(fname_excel, engine='xlsxwriter')

        for pre_mask_type in pre_mask_types:
            for unit in units:
                name_mask_unit = pre_mask_type + unit

                df_save = pd.DataFrame(data=dfs_stat[name_gtc_param][name_mask_unit])  # create data frame
                df_save = df_save.sort_values(by='genes')

                sheet_name = name_mask_unit.replace('in ', '')  # length of name of sheet must be <31 chars
                sheet_name = sheet_name.replace(' [-]', '')  # Invalid Excel character '[]:*?/\'
                sheet_name = sheet_name.replace(' [um-2]', '')
                sheet_name = sheet_name.replace('  ', ' ')  # Sheet name cannot start or end with an apostrophe

                if len(sheet_name) > 31:
                    raise ValueError("Excel worksheet name must be <= 31 chars:\n"
                                     "Sheetname: '%s' has the length %d" % (sheet_name, len(sheet_name)))

                df_save.to_excel(excel_file, sheet_name=sheet_name, index=False)

        excel_file.save()

#################################
