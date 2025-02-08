# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:21:27 2023

@author: ayhyd
"""

import pandas as pd
import numpy as np
import cigsatbuf_utils.DM_files2 as DM_files2
from os import path, mkdir


def adjust_format(astring, number_of_spaces):
    '''Adjust the format of a string to match the number of spaces alocated'''
    return (' ' * number_of_spaces)[:-len(str(astring))] + str(astring)


def adjust_sin_file(sin_file, output_SIN_file, threshold_depth=90):
    '''Sets the values of upflux to zeros for the depths deeper than the specified depth.
    Creates a new SIN file at the output_folder location'''
    infile = open(sin_file, "r")
    outfile = open(output_SIN_file, "w")
    i = 0
    num_of_wrc_pts = -999
    num_of_upflux_pts = -999
    for line in infile:
        if i == 1:
            num_of_wrc_pts = int(line.strip()[:2])
            num_of_upflux_pts = int(line.strip()[2:])

        if i > num_of_wrc_pts + 1 and i <= num_of_wrc_pts + num_of_upflux_pts + 1:
            cur_depth_value = round(float(line.split()[0]), 1)
            if cur_depth_value >= threshold_depth:
                depth = round(float(line.split()[0]), 1)
                vol = round(float(line.split()[1]), 3)
                upflux = 0
                line = adjust_format(f"{depth:.4f}", 10) + adjust_format(f"{vol:.4f}", 10) + adjust_format(
                    f"{upflux:.4f}", 10) + '\n'

        i += 1
        outfile.write('{}'.format(line))
    infile.close()
    outfile.close()


def calculate_area_weighted_average_DM_day_outputs(list_of_daily_DM_files, original_list_of_area_percents,
                                                   start_year, end_year):
    '''identifies the output daily DRAINMOD hydrology files that have complete number of records
    so as to use them later jn the area-weighted average calculations to aggregate the output daily DRAINMOD hydrology files
    of the different soils into a single file.
    The function only considers the output hydrology files with complete number of records
    when calculating the area-weighted average values of daily drainage discharge.
    returns a tuple of 3 elements.
    1) a list of the considered Mukey-Cokey combinations
    2) a list of the corresponding percentages of the total area of the considered Mukey-Cokey combinations
    3) a list of the corresponding pandas DataFrames of the daily records of the considered Mukey-Cokey combinations'''
    expected_number_of_records = len(pd.DataFrame(
        pd.date_range(start='1-1-{}'.format(start_year), end='12-31-{}'.format(end_year))))
    considered_dfs = []
    considered_percentage = []
    considered_components = []
    original_components = []

    list_of_area_percents = []
    if abs(100 - np.array(list_of_area_percents).sum()) / 100.0 > 0.01:
        print(
            " The sum of percentages is not really equal to 100 so distributing the remaining area percentage based on current percentages")
        list_of_area_percents = [round(x * 100 / np.array(original_list_of_area_percents).sum(), 2) for x in
                                 original_list_of_area_percents]

    for DM_file, apercent in zip(list_of_daily_DM_files, list_of_area_percents):
        combination = '_'.join(DM_file.split('/')[-1][:-4].split('_')[1:])
        original_components.append(combination)
        try:
            cur_df = DM_files2.read_DM_daily_file(DM_file)

            if len(cur_df) == expected_number_of_records:
                considered_dfs.append(cur_df)
                considered_percentage.append(apercent)
                considered_components.append(combination)
            else:
                print('Analyzed period is from year {} to year {}'.format(start_year, end_year))
                print("Number of reported daily records are not as expected")
                print("Output number of records = ", len(cur_df))
                print("Expected number of records = ", expected_number_of_records)
                print("for daily file")
                print(DM_file)
                cur_df = cur_df.set_index(pd.to_datetime(cur_df.DATE))
                cur_df.to_excel(r'C:\PhD\TD evaluate online SB tool/cur_df_DM.xlsx')
                ex_df = pd.DataFrame(
                    pd.date_range(start='1-1-{}'.format(start_year), end='12-31-{}'.format(end_year)))
                ex_df.columns = ['DATE']
                ex_df.to_excel(r'C:\PhD\TD evaluate online SB tool/ex_df.xlsx')
                print('missing records df')
                print(ex_df[~ ex_df.DATE.isin(cur_df.index)])

        except ValueError:
            print("Following DRAINMOD file has issue")
            print(DM_file)

    if len(original_components) != len(considered_components):
        print('Original components list is ', original_components)
        print('Considered components list in weighted average calculations of output hydrology values is \n',
              considered_components)
    return considered_components, considered_dfs, considered_percentage


def calculate_area_weighted_average_DM_yld_outputs(list_of_yld_DM_files, original_list_of_area_percents,
                                                   start_year, end_year):
    '''identifies the output daily DRAINMOD yield files that have complete number of records
    so as to use them later jn the area-weighted average calculations of yield to aggregate the output daily DRAINMOD
    yield files of the different soils into a single file.
    The function only considers the output yield files with complete number of records
    when calculating the area-weighted average values of relative yield.
    returns a tuple of 3 elements.
    1) a list of the considered Mukey-Cokey combinations
    2) a list of the corresponding percentages of the total area of the considered Mukey-Cokey combinations
    3) a list of the corresponding pandas DataFrames of the daily records of the considered Mukey-Cokey combinations'''

    number_years = int(end_year - start_year) + 1
    considered_df_lists = []
    considered_percentage = []
    considered_components = []
    list_of_area_percents = []
    if abs(100 - np.array(list_of_area_percents).sum()) / 100.0 > 0.01:
        print(
            " The sum of percentages is not really equal to 100 so distributing the remaining area percentage based on current percentages")
        list_of_area_percents = [round(x * 100 / np.array(original_list_of_area_percents).sum(), 2) for x in
                                 original_list_of_area_percents]

    for DM_file, apercent in zip(list_of_yld_DM_files, list_of_area_percents):
        combination = '_'.join(DM_file.split('/')[-1][:-4].split('_')[1:])
        try:
            cur_df_list = DM_files2.read_yld_file(DM_file)
            yld_years = int(sum([len(x) for x in cur_df_list]))

            if yld_years == number_years:
                considered_df_lists.append(cur_df_list)
                considered_percentage.append(apercent)
                considered_components.append(combination)
            else:
                print("Number of reported yld years are not as expected")
                print("yld_years = ", yld_years)
                print("number_years = ", number_years)
                print("for yld file")
                print(DM_file)
        except ValueError:
            print("Following DRAINMOD file has issue")
            print(DM_file)

    return considered_components, considered_df_lists, considered_percentage


def get_dict_of_DM_files(alocation, DRAINMOD_output_folder, list_of_mukey_cokey_tuples, file_ext=['GRD', 'YLD']):
    '''
    Example format of list_of_mukey_cokey_tuples is ((406454, 22052368), (406502, 22052747), (406453, 22053011))'''
    output_dict = {'FD_day_files': [], 'FD_yld_files': [], 'CD_day_files': [], 'CD_yld_files': []}
    for acombination in list_of_mukey_cokey_tuples:
        mukey, cokey = acombination
        output_dict['FD_day_files'].append(
            r'{0}/{1}_{2}/FD_{1}_{2}.{3}'.format(DRAINMOD_output_folder, mukey, cokey, file_ext[0]))
        output_dict['CD_day_files'].append(
            r'{0}/{1}_{2}/CD_{1}_{2}.{3}'.format(DRAINMOD_output_folder, mukey, cokey, file_ext[0]))
        output_dict['FD_yld_files'].append(
            r'{0}/{1}_{2}/FD_{1}_{2}.{3}'.format(DRAINMOD_output_folder, mukey, cokey, file_ext[1]))
        output_dict['CD_yld_files'].append(
            r'{0}/{1}_{2}/CD_{1}_{2}.{3}'.format(DRAINMOD_output_folder, mukey, cokey, file_ext[1]))
    return output_dict


def define_components_with_valid_DM_outputs(considered_yld_components, considered_yld_df_lists,
                                            considered_yld_percentages,
                                            considered_day_components, considered_day_df_lists,
                                            considered_day_percentage):
    final_components = []
    final_yld_dfs_lists = []
    final_day_dfs_list = []
    final_percentages = []
    if len(considered_yld_df_lists) <= len(considered_day_df_lists):
        for i, acomponent in enumerate(considered_yld_components):
            if acomponent in considered_day_components:
                final_components.append(acomponent)
                target_index = considered_day_components.index(acomponent)
                final_yld_dfs_lists.append(considered_yld_df_lists[i])
                final_day_dfs_list.append(considered_day_df_lists[target_index])
                final_percentages.append(considered_yld_percentages[i])
    else:
        for i, acomponent in enumerate(considered_day_components):
            if acomponent in considered_yld_components:
                final_components.append(acomponent)
                target_index = considered_yld_components.index(acomponent)
                final_yld_dfs_lists.append(considered_yld_df_lists[target_index])
                final_day_dfs_list.append(considered_day_df_lists[i])
                final_percentages.append(considered_day_percentage[i])
    return final_components, final_day_dfs_list, final_yld_dfs_lists, final_percentages


def calc_area_weighted_average_DM_yld_output(considered_df_lists, considered_percentage):
    final_list = []
    considered_percentage = [round(p * 100 / (sum(considered_percentage)), 2) for p in considered_percentage]
    for cur_df_list, apercent in zip(considered_df_lists, considered_percentage):

        if len(final_list) == 0:
            final_list = [cur_df_list[0].loc[:, :] * apercent / 100.0,
                          cur_df_list[1].loc[:, :] * apercent / 100.0]
        else:
            final_list[0] += cur_df_list[0].loc[:, :] * apercent / 100.0
            final_list[0].loc[:, :] = final_list[0].loc[:, :].apply(lambda x: round(x, 1))
            final_list[1] += cur_df_list[1].loc[:, :] * apercent / 100.0
            final_list[1].loc[:, :] = final_list[1].loc[:, :].apply(lambda x: round(x, 1))
    return final_list


def calc_area_weighted_average_DM_day_output(considered_dfs, considered_percentage):
    final_df = pd.DataFrame()
    considered_percentage = [round(p * 100 / (sum(considered_percentage)), 2) for p in considered_percentage]
    for i, cur_df in enumerate(considered_dfs):
        apercent = considered_percentage[i]
        cur_columns_to_change = cur_df.columns[4:]
        cur_df.loc[:, cur_columns_to_change] = cur_df.loc[:, cur_columns_to_change] * apercent / 100.0
        if final_df.shape[0] == 0:
            final_df = cur_df
        else:
            final_df.loc[:, cur_columns_to_change] += cur_df.loc[:, cur_columns_to_change]
    return final_df


def get_area_weighted_df_DM_day(alocation, DRAINMOD_output_folder, output_folder, list_of_mukey_cokey_tuples,
                                list_of_area_percents, AOFI, start_year, end_year, check_yield=True,
                                write_excel=True):
    '''saves excel sheets of the average-weighted output values of drainage discharges
    for each drainage mode free drainage (FD) and Controlled drainage (CD).
    returns a dictionary with 2 keys that has pandas DataFrames of the average-weighted output values
    of drainage discharges for each drainage mode free drainage (FD) and Controlled drainage (CD).
    if check_yield is set to True. it will consider the DRAINMOD yld outputs on top of the previously
    explained parameter for each mode FD and CD
    alocation: is an ID
    AOFI: area of field of interest in ha
    Example format of list_of_area_percents is (44.61, 43.71, 11.68)'''
    dfs_dict = {'FD_day_df': None, 'FD_yld_df': None, 'CD_day_df': None, 'CD_yld_df': None}
    DM_outputfiles_dict = get_dict_of_DM_files(alocation, DRAINMOD_output_folder, list_of_mukey_cokey_tuples)
    list_of_FD_daily_DM_files = DM_outputfiles_dict['FD_day_files']
    list_of_CD_daily_DM_files = DM_outputfiles_dict['CD_day_files']
    list_of_FD_yld_DM_files = DM_outputfiles_dict['FD_yld_files']
    list_of_CD_yld_DM_files = DM_outputfiles_dict['CD_yld_files']
    coef_ha_to_cm2 = 10 ** 8  # to transform from ha to cm2

    if write_excel:
        if not path.exists(output_folder):
            mkdir(output_folder)

    if check_yield:
        FD_considered_yld_components, FD_considered_yld_df_lists, FD_considered_yld_percentages = calculate_area_weighted_average_DM_yld_outputs(
            list_of_FD_yld_DM_files, list_of_area_percents, start_year, end_year)
        CD_considered_yld_components, CD_considered_yld_df_lists, CD_considered_yld_percentages = calculate_area_weighted_average_DM_yld_outputs(
            list_of_CD_yld_DM_files, list_of_area_percents, start_year, end_year)

        FD_considered_day_components, FD_considered_day_df_lists, FD_considered_day_percentages = calculate_area_weighted_average_DM_day_outputs(
            list_of_FD_daily_DM_files, list_of_area_percents, start_year, end_year)

        CD_considered_day_components, CD_considered_day_df_lists, CD_considered_day_percentages = calculate_area_weighted_average_DM_day_outputs(
            list_of_CD_daily_DM_files, list_of_area_percents, start_year, end_year)

        FD_final_components, FD_final_day_dfs_list, FD_final_yld_dfs_lists, FD_final_percentages = define_components_with_valid_DM_outputs(
            FD_considered_yld_components, FD_considered_yld_df_lists, FD_considered_yld_percentages,
            FD_considered_day_components, FD_considered_day_df_lists, FD_considered_day_percentages)

        CD_final_components, CD_final_day_dfs_list, CD_final_yld_dfs_lists, CD_final_percentages = define_components_with_valid_DM_outputs(
            CD_considered_yld_components, CD_considered_yld_df_lists, CD_considered_yld_percentages,
            CD_considered_day_components, CD_considered_day_df_lists, CD_considered_day_percentages)

        dfs_dict['FD_day_df'] = calc_area_weighted_average_DM_day_output(
            FD_final_day_dfs_list, FD_final_percentages)
        dfs_dict['CD_day_df'] = calc_area_weighted_average_DM_day_output(
            CD_final_day_dfs_list, CD_final_percentages)
        dfs_dict['FD_day_df'].to_excel(r'{}/FD_day_{}.xlsx'.format(output_folder, alocation), index=False)
        dfs_dict['CD_day_df'].to_excel(r'{}/CD_day_{}.xlsx'.format(output_folder, alocation), index=False)
    else:
        CD_final_day_components, CD_final_day_dfs_list, CD_final_percentages = calculate_area_weighted_average_DM_day_outputs(
            list_of_CD_daily_DM_files, list_of_area_percents, start_year, end_year)

        dfs_dict['CD_day_df'] = calc_area_weighted_average_DM_day_output(
            CD_final_day_dfs_list, CD_final_percentages)
        if write_excel:
            dfs_dict['CD_day_df'].to_excel(r'{}/CD_day_{}.xlsx'.format(output_folder, alocation), index=False)

    if check_yield:
        dfs_dict['FD_yld_files'] = calc_area_weighted_average_DM_yld_output(
            FD_final_yld_dfs_lists, FD_final_percentages)

        dfs_dict['CD_yld_files'] = calc_area_weighted_average_DM_yld_output(
            CD_final_yld_dfs_lists, CD_final_percentages)
        DM_files2.DRAINMOD_yearly_yld_to_excel(dfs_dict['FD_yld_files'], output_folder, 'FD_yld_{}'.format(alocation))
        DM_files2.DRAINMOD_yearly_yld_to_excel(dfs_dict['CD_yld_files'], output_folder, 'CD_yld_{}'.format(alocation))

    if type(AOFI) == tuple:
        if check_yield:
            for amode in ('FD', 'CD'):
                dfs_dict['{}_day_df'.format(amode)]['QDD'] = np.nan
                dfs_dict['{}_day_df'.format(amode)] = dfs_dict['{}_day_df'.format(amode)].set_index(
                    pd.to_datetime(dfs_dict['{}_day_df'.format(amode)]['DATE']))
                negative_DDCD_filter = dfs_dict['{}_day_df'.format(amode)][
                                           'DDCD'] < 0  # filter for days with subirrigation. negative drainage values
                dfs_dict['{}_day_df'.format(amode)].loc[dfs_dict['{}_day_df'.format(amode)][
                    negative_DDCD_filter].index, 'DDCD'] = 0  # disregard subirrigation days sets their values to 0
                for ayear_range in AOFI:
                    cur_area = ayear_range[0]
                    cur_start_year = str(ayear_range[1])
                    cur_end_year = str(ayear_range[2])
                    dfs_dict['{}_day_df'.format(amode)].loc[cur_start_year: cur_end_year, 'QDD'] = dfs_dict[
                                                                                                       '{}_day_df'.format(
                                                                                                           amode)].loc[
                                                                                                   cur_start_year: cur_end_year,
                                                                                                   'DDCD'] * coef_ha_to_cm2 * cur_area  # drainage values are transformed to cm3/day
                if write_excel:
                    dfs_dict['{}_day_df'.format(amode)][['year', 'month', 'day', 'QDD']].to_excel(
                        '{}/{} daily hydrology.xlsx'.format(output_folder, '{}_{}_input'.format(alocation, amode)),
                        index=False)
        else:
            dfs_dict['CD_day_df']['QDD'] = np.nan
            dfs_dict['CD_day_df'] = dfs_dict['CD_day_df'].set_index(pd.to_datetime(dfs_dict['CD_day_df']['DATE']))
            negative_DDCD_filter = dfs_dict['CD_day_df'][
                                       'DDCD'] < 0  # filter for days with subirrigation. negative drainage values
            dfs_dict['CD_day_df'].loc[dfs_dict['CD_day_df'][
                negative_DDCD_filter].index, 'DDCD'] = 0  # disregard subirrigation days sets their values to 0
            for ayear_range in AOFI:
                cur_area = ayear_range[0]
                cur_start_year = str(ayear_range[1])
                cur_end_year = str(ayear_range[2])
                dfs_dict['CD_day_df'].loc[cur_start_year: cur_end_year, 'QDD'] = dfs_dict['CD_day_df'].loc[
                                                                                 cur_start_year: cur_end_year,
                                                                                 'DDCD'] * coef_ha_to_cm2 * cur_area  # drainage values are transformed to cm3/day

    else:
        ha_to_ac = 2.47105
        if check_yield:
            for amode in ('FD', 'CD'):
                dfs_dict['{}_day_df'.format(amode)]['QDD'] = np.nan
                dfs_dict['{}_day_df'.format(amode)] = dfs_dict['{}_day_df'.format(amode)].set_index(
                    pd.to_datetime(dfs_dict['{}_day_df'.format(amode)]['DATE']))
                negative_DDCD_filter = dfs_dict['{}_day_df'.format(amode)][
                                           'DDCD'] < 0  # filter for days with subirrigation. negative drainage values
                dfs_dict['{}_day_df'.format(amode)].loc[dfs_dict['{}_day_df'.format(amode)][
                    negative_DDCD_filter].index, 'DDCD'] = 0  # disregard subirrigation days sets their values to 0

                dfs_dict['{}_day_df'.format(amode)].loc[:, 'QDD'] = dfs_dict['{}_day_df'.format(amode)].loc[:,
                                                                    'DDCD'] * coef_ha_to_cm2 * AOFI  # drainage values are transformed to cm3/day
                if write_excel:
                    dfs_dict['{}_day_df'.format(amode)][['year', 'month', 'day', 'QDD']].to_excel(
                        '{}/{} daily hydrology.xlsx'.format(output_folder, '{}_{}_input'.format(alocation, amode)),
                        index=False)
        else:
            dfs_dict['CD_day_df']['QDD'] = np.nan
            dfs_dict['CD_day_df'] = dfs_dict['CD_day_df'].set_index(pd.to_datetime(dfs_dict['CD_day_df']['DATE']))
            negative_DDCD_filter = dfs_dict['CD_day_df'][
                                       'DDCD'] < 0  # filter for days with subirrigation. negative drainage values
            dfs_dict['CD_day_df'].loc[dfs_dict['CD_day_df'][
                negative_DDCD_filter].index, 'DDCD'] = 0  # disregard subirrigation days sets their values to 0
            dfs_dict['CD_day_df'].loc[:, 'QDD'] = dfs_dict['CD_day_df'].loc[:,
                                                  'DDCD'] * coef_ha_to_cm2 * AOFI  # drainage values are transformed to cm3/day

            if write_excel:
                if not path.exists(output_folder):
                    mkdir(output_folder)
                print(dfs_dict['FD_day_df'].head())
                # print(dfs_dict.keys())
                DM_files2.DRAINMOD_daily_hydrology_to_excel(dfs_dict['FD_day_df'],
                                                            AOFI * ha_to_ac, output_folder,
                                                            '{}_FD_input'.format(alocation))
                DM_files2.DRAINMOD_daily_hydrology_to_excel(dfs_dict['CD_day_df'],
                                                            AOFI * ha_to_ac, output_folder,
                                                            '{}_CD_input'.format(alocation))

    return dfs_dict

