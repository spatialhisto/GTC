#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.post_proc as g_post
from scipy import stats


def summarize_t_tests(
    fnames_gtc_param: list,
    genes: list,
    column_names: list,
    dict_disease_history: dict,
    dfs_counts: dict
) -> dict:

    """Perform two statitical tests with
    the data:
     - two-sided paired t-test for gene
       distribution in 'neoplastic' and
       'non-neoplastic' tissue and
     - two-sided independent t-test for
       gene distribution in 'neoplastic'
       tissue in respect of the disease
       history of the patients.
    and summarize the output in a data
    frame.

    See also:
     - Wilcoxon test: test used when the prerequisites
       for a dependent-samples t-test are not met
       with scipy.stats.wilcoxon.
     - Shapiro-Wilk test: test that the underlying
       population of a sample is normally distributed
       with scipy.stats.shapiro."""

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    pre_mask_types, tissues, units = g_post.split_column_names_in_mask_types_and_tissues_and_units(column_names)

    dfs_stat = g_post.build_stat_test_dict(names_gtc_param, pre_mask_types, units)

    for name_gtc_param in names_gtc_param:
        print('-Summary for %s' % name_gtc_param)

        for pre_mask_type in pre_mask_types:
            for unit in units:
                df = pd.DataFrame(np.nan, index=range(0, len(genes)),
                                  columns=['genes',
                                           'ttest_rel_statistic', 'ttest_rel_pvalue',
                                           'ttest_rel_mean1', 'ttest_rel_mean2',
                                           'ttest_ind_statistic', 'ttest_ind_pvalue',
                                           'ttest_ind_mean1', 'ttest_ind_mean2'])
                df['genes'] = genes

                for gene in genes:

                    ##################################################################
                    # Test that the gene distribution does not differ in normal and
                    #  neoplastic tissue with not distinguishing between relaps yes/no
                    # d_n = c1_n - c2_n for paired samples c1 and c2
                    # Null hypothesis (H0): µ_d = 0, for e.g. alpha = 0.05
                    # Alternative hypothesis (HA): µd ≠ 0
                    # Perform 2-sided paired t-test
                    # Output:
                    # - statistics: equal to z-score
                    # - pvalue: if pavlue >= alpha / 2, except H0
                    #           if pvalue  < alpha / 2, reject H0
                    # NOTE: alpha not need for pvalue calculation
                    ##################################################################

                    def get_counts(tissue):
                        column_name = pre_mask_type + tissue + unit
                        index = g_post.get_row_index(dfs_counts[name_gtc_param][column_name], 'genes', gene)
                        gene_counts = dfs_counts[name_gtc_param][column_name].iloc[index, 1:]  # ignore column with gene names
                        return gene_counts

                    data1 = get_counts("'neoplastic'")
                    data2 = get_counts("'non-neoplastic'")

                    statistic, pvalue = stats.ttest_rel(data1, data2, alternative='two-sided', nan_policy='propagate')

                    index = g_post.get_row_index(df, 'genes', gene)
                    df.at[index, 'ttest_rel_statistic'] = statistic
                    df.at[index, 'ttest_rel_pvalue'] = pvalue
                    df.at[index, 'ttest_rel_mean1'] = np.mean(data1)
                    df.at[index, 'ttest_rel_mean2'] = np.mean(data2)

                    #######################################################################
                    # Test that the gene distribution does not differ in neoplastic tissues
                    #  with distinguishing between patient relaps cases yes/no
                    # Null hypothesis H0: µ1 = µ2, for e.g. alpha = 0.05
                    # Alternative hypothesis (HA): µ1 ≠ µ2
                    # Perform 2-sided independent t-test with equal variances
                    # Rule of thumb: assume the populations have equal variances if the
                    #  ratio variances σ1 / σ2 < 4 (otherwise a Welsch test is performed)
                    # Output:
                    # - statistics: equal to z-score
                    # - pvalue: if pavlue >= alpha / 2, except H0
                    #           if pvalue  < alpha / 2, reject H0
                    # NOTE: alpha not need for pvalue calculation
                    #######################################################################

                    column_name = pre_mask_type + "'neoplastic'" + unit
                    index = g_post.get_row_index(dfs_counts[name_gtc_param][column_name], 'genes', gene)
                    gene_counts = dfs_counts[name_gtc_param][column_name].iloc[index, 1:]  # ignore column with gene names
                    samples = dfs_counts[name_gtc_param][column_name].columns[1:]  # ignore column with gene names

                    def split_gene_counts_relating_to_relaps(relaps):
                        data = [count for (count, sample) in zip(gene_counts, samples)
                                if dict_disease_history[sample] == relaps]
                        return data

                    data1 = split_gene_counts_relating_to_relaps('yes')
                    data2 = split_gene_counts_relating_to_relaps('no')

                    if len(data1) > 1 and len(data2) > 1:  # enough values for variance calculation
                        var1 = np.var(data1)
                        var2 = np.var(data2)

                        equal_var = True if max(var1, var2) / min(var1, var2) < 4 else False  # rule of thumb

                        statistic, pvalue = stats.ttest_ind(data1, data2, equal_var=equal_var, alternative='two-sided',
                                                            nan_policy='propagate')

                        index = g_post.get_row_index(df, 'genes', gene)
                        df.at[index, 'ttest_ind_statistic'] = statistic
                        df.at[index, 'ttest_ind_pvalue'] = pvalue
                        df.at[index, 'ttest_ind_mean1'] = np.mean(data1)
                        df.at[index, 'ttest_ind_mean2'] = np.mean(data2)

                dfs_stat[name_gtc_param][pre_mask_type + unit] = df

    return dfs_stat

#################################
