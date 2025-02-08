# This script completes Step A, Phase one of BAE-CIG Saturated Buffer:
# For each county (start with Lenawee County, MI), there are Map Units. For each Map Unit,
# determine the components flagged as "Major components".
# Only major components will be considered and minor components will be ignored.
#
# Use representative values for
#
# Total Sand% (sandtotal_r)
# Total Silt%  (silttotal_r)
# Total Clay% (claytotal_r)
# Bulk density (dbthirdbar_r)
# volumetric FC (wthirdbar_r)
# volumetric PWP (wfifteenbar_r)
import os
import pandas as pd
import shutil
import pyodbc
from glob import glob
from cigsatbuf_utils.envs import SAMPLES_DIR

# Keys are the names of the tables of interest
# each key maps to a list of columns of interest
# specifically, each key maps to a dictionary containing the actual labels (in the Access files) and the aliases of
# these labels (as found in the exported Excel files).
TABLE_MAP_COLS = {

    'mapunit': {'names': ['Mapunit Key', 'Mapunit Symbol', 'Mapunit Name'],
                'aliases': ['muname', 'mukey'],
                },

    'component': {
        'names': ['Component Key', 'Component Name', 'Hydrologic Group', 'Slope Gradient - Representative Value',
                  'Comp % - Representative Value', 'Drainage Class'],

        'aliases': ['mukey', 'cokey', 'majcompflag', 'compname', 'drainagecl'],
    },

    'corestrictions': {'names': [],
                       'aliases': ['resdept_r', 'corestrictkey', 'cokey', ],
                       },

    'chorizon': {'names': ['Chorizon Key', 'Bottom Depth - Representative Value', 'Total Sand - Representative Value',
                           'Total Silt - Representative Value', 'Total Clay - Representative Value',
                           'OM - Representative Value', 'Db 0.33 bar H2O - Representative Value',
                           'Ksat - Representative Value', 'PI - Representative Value', 'LL - Representative Value'],

                 'aliases': ['wfifteenbar_r', 'wthirdbar_r', 'wsatiated_r', 'ksat_r', 'dbthirdbar_r', 'om_r',
                             'sandtotal_r', 'silttotal_r', 'claytotal_r', 'hzdepb_r', 'cokey', 'chkey', ]
                 },
}

SOURCES = ['db', 'excel']
REPRESENTATIVE_COLS = ['sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'wthirdbar_r', 'wfifteenbar_r']

def extract_soil_inputs_from_db():
    """
    Incomplete function. Meant to return an Excel file containing the aliases columns of TABLE_MAP_COLS
    :return:
    """
    soil_db_path = glob("data/*/*.mdb")

    if len(soil_db_path) == 0:
        print("No database files found. Please check. Exiting...")
        exit()

    if len(soil_db_path) > 1:
        print("Probably several database files found. Must be only one. Exiting...")
        exit()

    soil_db_path_dbq = f"DBQ={soil_db_path[0]};"

    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={soil_db_path[0]};'
    )

    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()

    for table_info in crsr.tables(tableType='TABLE'):
        print(table_info.table_name)


def remove_incomplete_rows(df_obj, condition_columns=REPRESENTATIVE_COLS):
    """
    Remove rows where any of condition_columns is missing
    :param df_obj: pandas dataframe
    :param condition_columns: a list of pandas columns
    :return: a dataframe
    """
    has_missing_values = df_obj.index[df_obj[condition_columns].isnull().any(axis=1)]
    df_obj.drop(has_missing_values, axis=0, inplace=True)
    return df_obj


def fill_in_missing_values(df_obj, column='resdept_r', sub=305, condition_num=200):
    """
    Whenever the depth to restrictive layer of SSURGO_D is greater than 200 cm or it's missing,
    use a depth to restrictive layer of 305 cm
    :param df_obj: pandas dataframe
    :param column:
    :param sub: the value to subsitute missing values by
    :param condition_num: condition to check for while replacing missing value
    :return: pandas dataframe
    """
    df_obj_ = df_obj.copy()
    df_obj_[column] = df_obj_[column].fillna(sub)
    case_gt_condition_num = [sub if val > condition_num else val for val in df_obj_[column]]
    df_obj_[column] = case_gt_condition_num
    return df_obj_


def format_output_for_stepA_task1(df_major_components):
    """
    Yousef required the output file to be like this to match Rosetta's requirements in Rpredict.py

    :param df_major_components:
    :return: a formatted dataframe object
    """
    df_temp = pd.DataFrame()
    df_temp['sand'] = df_major_components['sandtotal_r']
    df_temp['silt'] = df_major_components['silttotal_r']
    df_temp['clay'] = df_major_components['claytotal_r']
    df_temp['bulk density'] = df_major_components['dbthirdbar_r']
    df_temp['water content FC'] = df_major_components['wthirdbar_r']
    df_temp['water content PWP'] = df_major_components['wfifteenbar_r']
    df_temp['map unit key'] = df_major_components['mukey']
    df_temp['coKey'] = df_major_components['cokey']
    df_temp['layer'] = df_major_components['hzdepb_r']

    df_temp['map unit name'] = df_major_components['muname']
    df_temp['saturated hydraulic conductivity'] = df_major_components['ksat_r']
    df_temp['Depth to restrictive layer'] = df_major_components['resdept_r']
    df_temp['water content top layer'] = df_major_components['wsatiated_r']

    return df_temp


def extract_soil_inputs_from_tables(task='1', data_input_dir='.'):
    """
    :param data_input_dir:
    :param task: a string - refers to step A, task #. Is either '1' or '4' (default value is '1')
    :return: a dataframe object containing the major components of soil information
    """

    def get_cols_oi(county_name, colname):
        col_without_county_name = colname.split("_")[-1]
        return pd.read_excel(tables_map_file[f"{county_name}_{colname}"])[TABLE_MAP_COLS[colname]['aliases']]

    county_name = str(data_input_dir).split(os.sep)[-1]
    xls_files = glob(os.path.join(data_input_dir, "*.xlsx"))
    if len(xls_files) == 0:
        raise FileNotFoundError(f"No Excel files found in {data_input_dir}")

    tables_map_file = dict([(str(file_path).split(os.sep)[-1][:-5], file_path) for file_path in xls_files])
    soil_tables_path = tables_map_file.values()
    # print(f"{tables_map_file = }")

    # Making sure the excel files of the tables of interest are all present on disk
    all_tables_present = all(t.split("_")[-1] in TABLE_MAP_COLS.keys() for t in tables_map_file.keys())

    if not all_tables_present:
        print(f"Some of the tables are missing. Need excel files for each of the following: {TABLE_MAP_COLS.keys()}")
        raise FileNotFoundError(f"Some of the tables are missing. Need excel files for each of the following: {TABLE_MAP_COLS.keys()}")

    # aliases_cols = [el for dict_i in TABLE_MAP_COLS.values() for el in dict_i['aliases']]
    df_component = get_cols_oi(county_name, "component")
    df_major_components = df_component[df_component['majcompflag'] == 'Yes']

    df_corestrictions = get_cols_oi(county_name, "corestrictions")
    df_chorizon = get_cols_oi(county_name, "chorizon")
    df_mapunit = get_cols_oi(county_name, "mapunit")

    df_major_components = pd.merge(df_major_components, df_corestrictions, how="left", on="cokey")
    df_major_components = pd.merge(df_major_components, df_chorizon, how="left", on="cokey")
    df_major_components = pd.merge(df_major_components, df_mapunit, how="left", on="mukey")

    if task == '1':
        selective_columns = ['dbthirdbar_r', 'silttotal_r', 'cokey', 'mukey', 'resdept_r', 'sandtotal_r',
                             'wsatiated_r', 'wthirdbar_r', 'claytotal_r', 'wfifteenbar_r', 'ksat_r', 'hzdepb_r',
                             'muname']
    elif task == '4':
        selective_columns = ['cokey', 'mukey', 'wfifteenbar_r', 'wthirdbar_r', 'resdept_r',
                             'hzdepb_r', 'ksat_r', 'wsatiated_r', ]
    elif task == '5':
        selective_columns = ['cokey', 'mukey', 'muname', 'compname', 'sandtotal_r', 'silttotal_r', 'claytotal_r', 'wsatiated_r',
                             'dbthirdbar_r', 'wthirdbar_r', 'wfifteenbar_r', 'resdept_r', 'ksat_r', 'hzdepb_r', 'drainagecl']
    else:
        selective_columns = [el for dict_i in TABLE_MAP_COLS.values() for el in dict_i['aliases']]

    df_major_components = df_major_components[selective_columns]

    # round to 5 decimal places
    df_major_components = df_major_components.round(5)

    # deal with missing value in resdept_r specifically:
    df_major_components = fill_in_missing_values(df_major_components)
    # deal with other missing data:
    df_major_components = remove_incomplete_rows(df_major_components)

    if task == '5':
        return df_major_components

    # Convert the layer column into integer, after removing NaN values from step above
    df_major_components['hzdepb_r'] = df_major_components['hzdepb_r'].astype(int)

    return format_output_for_stepA_task1(df_major_components)


def extract_soil_inputs(output_fpath, access_db_dir, source='excel'):
    """
    CSV file containing the aliases columns of TABLE_MAP_COLS

    :param source: source: either 'db', or 'excel'
    :param output_str:
    :return: representative_soil_inputs.xlsx | None
    """
    if source not in SOURCES:
        print(f"'source' parameter must be one of {SOURCES}")
        return

    if source == 'excel':
        if os.path.exists(output_fpath):
            print(f"File already exists: {output_fpath}")
            return pd.read_excel(output_fpath), output_fpath

        output_df = extract_soil_inputs_from_tables(task='1', data_input_dir=access_db_dir)
        output_df.to_excel(output_fpath, index=False)
        shutil.copy(output_fpath, SAMPLES_DIR)
        return output_df, output_fpath
    elif source == 'db':
        raise NotImplementedError("This function is not yet implemented")

