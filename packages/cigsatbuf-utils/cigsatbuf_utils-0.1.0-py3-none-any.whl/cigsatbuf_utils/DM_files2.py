# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 12:57:15 2022

@author: Yousef abdalaal
email : ay.hydrogis@gmail.com, abdalaal@msu.edu
"""
## The functions defined in this module can do the following :
# 1- Read DRAINMOD output files of the daily hydrology and yield and return the
#    data as pandas dataframes
# 2- Saves the created pandas DataFrame from step 1 to excel sheets

# Section 1 defines libraries that will be used in the python code
import datetime as dt
from datetime import timedelta
import pandas as pd

##########################################################################################################################################
##########################################################################################################################################
# This Section defines functions related to reading in output from DRAINMOD model

def read_DM_file(DM_file):
    '''Reads DRAINMOD daily file path. Returns a pandas dataframe of daily data'''
    infile = open(DM_file, "r")
    # Structure of DRAINMOD daily file
    # year Month
    # Day Rain Infil ET Drainage Total_volume DDZ  WTdepth Stor Runoff Water_loss
    # the header lines are 18 lines. data starts after line 18
    dd=[]
    l = 1
    for line in infile:
        if l > 18 :
            cur_line = line.strip()
            cur_line_items = cur_line.split()
            if len(cur_line_items) == 2:
                cur_year  = int(cur_line_items[0])
                cur_month  = int(cur_line_items[1])
            elif len(cur_line_items) ==0:
                None
            elif len(cur_line_items) ==1:
                None
            elif cur_line_items[0] == "DAY":
                None
            else:
                cur_day = int(cur_line_items[0])
                cur_rain = float(cur_line_items[1])
                cur_infiltration = float(cur_line_items[2])
                cur_et = float(cur_line_items[3])
                cur_drainage = float(cur_line_items[4])
                cur_total_vol = float(cur_line_items[5])
                cur_ddz = float(cur_line_items[6])
                cur_wtd = float(cur_line_items[7])
                cur_stor = float(cur_line_items[8])
                cur_runoff = float(cur_line_items[9])
                cur_wloss = float(cur_line_items[10])
                try:
                    cur_SLOPSP = float(cur_line_items[11])
                    cur_VERTSP = float(cur_line_items[12])
                    cur_LATSP = float(cur_line_items[13])
                    dd.append([dt.date(cur_year, cur_month, cur_day),
                               cur_year, cur_month, cur_day,
                               cur_rain, cur_infiltration, cur_et, cur_drainage,
                               cur_total_vol, cur_ddz, cur_wtd, cur_stor, cur_runoff,
                               cur_wloss, cur_SLOPSP, cur_VERTSP, cur_LATSP])
                except:
                    dd.append([dt.date(cur_year, cur_month, cur_day),
                               cur_year, cur_month, cur_day, cur_rain,
                               cur_infiltration, cur_et, cur_drainage, cur_total_vol,
                               cur_ddz, cur_wtd, cur_stor, cur_runoff, cur_wloss])
        l+=1
    infile.close()
    p=pd.DataFrame(dd)
    try:
        p.columns =['DATE', 'year','month','day', 'RAIN', 'INFILT', 'ET', 'DDCD', 'TVOL',
                    'DDZ', 'WTD','STOR', 'RO', 'WLOSS', 'SLOPSP', 'VERTSP', 'LATSP']
    except:
        p.columns =['DATE', 'year','month','day', 'RAIN', 'INFILT', 'ET', 'DDCD',
                    'TVOL', 'DDZ', 'WTD', 'STOR', 'RO', 'WLOSS']
    pp = p.sort_index()
    return pp

def read_yld_file(DM_file):
    '''Reads DRAINMOD yld file path. Returns a pandas dataframe of yearly relativel yld'''
    infile = open(DM_file, "r")
    # Structure of DRAINMOD daily file
    # year Month
    # Day Rain Infil ET Drainage Total_volume DDZ  WTdepth Stor Runoff Water_loss
    # the header lines are 18 lines. data starts after line 18
    d={}
    l = 1
    columns_line = False
    for line in infile:
        if columns_line == True:
            l +=1
        line_list = line.strip().split()
        if len(line_list) > 4:
            if line_list[0]== 'SDI' and line_list[2]== 'STRESS' and line_list[-1]== '(%)' and line_list[-2]== 'YIELDS':
                columns_line = True
                
            if l>3 and line_list[0] == 'AVG':
                print("Long term average yield is ", line_list[-1], "%")
            elif l>3 and type(int(line_list[0])) == int:
                cur_year = int(line_list[0])
                cur_yld = float(line_list[-1])
                d[dt.date(cur_year, 12, 31)]= [cur_yld]      

    infile.close()
    p=pd.DataFrame.from_dict(d, orient='index')
    p.columns =['relative yield']
    pp = p.sort_index()
    return pp
###########################################################################################################################
###########################################################################################################################
#This section defines functions for creating excel sheets of the Dataframes created in step 1
##########################################################################################################################
def DRAINMOD_daily_hydrology_to_excel(df, AOFI, output_folder, ID):
    '''Creates excel sheet for the daily hydrology data from DRAINMOD. The structure of the sheet is:
        year month day and QDD columns. QDD values are in cm3/day. ID is an identifier to differentiate
        between saved files of FD and CD'''
    coef_ac_to_cm2 = 40468564.224 # to transform from ac to cm2
    negative_DDCD_filter = df['DDCD'] < 0 # filter for days with subirrigation. negative drainage values
    df.loc[df[negative_DDCD_filter].index, 'DDCD'] = 0 # disregard subirrigation days sets their values to 0
    df['QDD'] = df['DDCD']*coef_ac_to_cm2*AOFI # drainage values are transformed to cm3/day
    df[['year', 'month', 'day', 'QDD']].to_excel(
        '{}{} daily hydrology.xlsx'.format(output_folder, ID), index=False)
    return df[['year', 'month', 'day', 'QDD']]


def DRAINMOD_yearly_yld_to_excel(df, output_folder, ID):
    '''Creates excel sheet for the yearly relative yield data from DRAINMOD. The structure of the sheet is:
        year and relative yield columns. relative yield values are in percentages. ID is an identifier
        to differentiate between saved files of FD and CD'''
    df.to_excel('{}{} yearly yield.xlsx'.format(output_folder, ID))
################################################################################
    
    