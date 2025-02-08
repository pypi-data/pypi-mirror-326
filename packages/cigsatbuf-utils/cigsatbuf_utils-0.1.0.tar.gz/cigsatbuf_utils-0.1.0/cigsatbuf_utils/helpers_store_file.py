# For each major component, create any file of your choice to store the "Map Unit Name" (muname) and "Compname" (
# compname) . For each soil layer, store the sand%, silt%, clay%, bulk density, Volumetric FC, and Volumetric PWP.
# For each "Map Unit Name" and "Compname", store the depth to restrictive layer (cm) aka resdept_r.
#
# What to extract: 'muname', 'compname', 'sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'wthirdbar_r',
# 'wfifteenbar_r', 'wsatiated_r', 'resdept_r' (and 'mukey' and 'cokey' just for the file)

import os
import numpy as np
import pandas as pd
from glob import glob
from cigsatbuf_utils.retrieve_soil_components import extract_soil_inputs_from_tables
from cigsatbuf_utils.helpers_gen_file import convert_ksat
from cigsatbuf_utils.envs import SAMPLES_DIR

FILE_NAME_CONVENTION = "{mukey}_{cokey}_{compname}_store.txt"
TASK_NO = '5'
FORMAT = '%-3i     %16.2f% 16.2f %15.2f %16.2f %10.2f %15.2f %15.2f %17.2f %13i     %+s'


def get_store_output_name(mukey, cokey, compname, rosfpath_list_oi):

    right_dir_name = f"{mukey}_{cokey}"
    for d in rosfpath_list_oi:
        if right_dir_name in d:
            out_dir = os.path.dirname(d)
            break
    fname = f"{right_dir_name}_{compname}_store.txt"
    out_file = os.path.join(out_dir, fname)
    return out_file


def create_store_file(df_row, cols_oi, ros_list_oi, rosfpath_list_oi, df_maj_comp_bkp):

    mukey = df_row['mukey']
    cokey = df_row['cokey']

    if f"{mukey}_{cokey}" not in ros_list_oi:
        print(f"Skipping {mukey}_{cokey} as it is not in the list of ROS files")
        return

    out_store_file = get_store_output_name(
        mukey,
        cokey,
        df_row['compname'],
        rosfpath_list_oi=rosfpath_list_oi
    )

    if os.path.exists(out_store_file):
        print(f"Skipping {mukey}_{cokey}*_store as the file already exists")
        return

    df_oi = df_maj_comp_bkp[
        (df_maj_comp_bkp['mukey'] == mukey) & (df_maj_comp_bkp['cokey'] == cokey)]

    df_oi = convert_ksat(df_oi)
    df_oi = df_oi.sort_values(by=['hzdepb_r'])
    data_out = df_oi[cols_oi].to_numpy()

    headline_columns = "     ".join(cols_oi) + "\n"
    with open(out_store_file, 'w') as fobj:
        fobj.write('Mukey: {} - Cokey: {} - {}\n'.format(mukey, cokey, df_row['muname']))
        fobj.write(headline_columns)
        np.savetxt(fobj, data_out, delimiter=',', fmt=FORMAT, )

    print(f"Task 5 - Store file created: {out_store_file}")




def combine_all_store_files(ros_sub_dir_parent_folder, state_county_id):
    # Get all the files in the directory
    all_store_files_matched = os.path.join(ros_sub_dir_parent_folder,"*", "*_store.txt")
    all_store_files_list = glob(all_store_files_matched)

    final_fpath = os.path.join(ros_sub_dir_parent_folder, "all_store_files_all_counties_summary.csv")
    mck2sc_fpath = os.path.join(ros_sub_dir_parent_folder, "mucokey_mapped_to_statecounties.csv")

    final_cols = ["mukey", "cokey", "muname", "hzdepb_r", "sandtotal_r", "silttotal_r", "claytotal_r", "dbthirdbar_r", "ksat_r", "wsatiated_r", "wthirdbar_r", "wfifteenbar_r", "resdept_r", "drainagecl"]

    mck2sc_data = []
    data = []
    for txt_f in all_store_files_list:

        with open(txt_f, mode='r') as fobj:
            lines = fobj.readlines()

            line1_split = lines[0].split()
            mukey, cokey = line1_split[1], line1_split[4]
            muname = " ".join(line1_split[6:])
            for i, line in enumerate(lines[2:]):
                line_split = line.split()
                data_for_this_dir = []
                if len(line_split) == 12:
                    drain_class = " ".join(line_split[-2:])
                    data_for_this_dir.extend(line_split[:-2])
                elif len(line_split) == 13:
                    drain_class = " ".join(line_split[-3:])
                    data_for_this_dir.extend(line_split[:-3])

                data_for_this_dir.append(drain_class)
                data_for_this_dir = [mukey, cokey, muname] + data_for_this_dir

                data.append(data_for_this_dir)
                mck2sc_data.append([mukey, cokey, state_county_id])
        # break

    data_df = pd.DataFrame(data, columns=final_cols)
    data_df["mukey"] = data_df["mukey"].astype(str)
    data_df["cokey"] = data_df["cokey"].astype(str)
    data_df.to_csv(final_fpath, index=False)

    mck2sc_data_df = pd.DataFrame(mck2sc_data, columns=["mukey", "cokey", "state_county_id"])
    mck2sc_data_df["mukey"] = mck2sc_data_df["mukey"].astype(str)
    mck2sc_data_df["cokey"] = mck2sc_data_df["cokey"].astype(str)
    mck2sc_data_df.to_csv(mck2sc_fpath, index=False)

    print(f"File(s) created: \n\t*{final_fpath}\n\t*{mck2sc_fpath}")





if __name__ == '__main__':
    files2consider_after_ros = r"output/ROS_FOLDERS_TO_KEEP.csv"
    df2process = pd.read_csv(files2consider_after_ros)
    rosfpath_list_oi = df2process['ros_fpath'].tolist()
    ros_list_oi = [os.path.basename(ros_fpath).replace("_setpB.ros", "") for ros_fpath in rosfpath_list_oi]

    task5_columns = ['hzdepb_r', 'sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'ksat_r', 'wsatiated_r',
                     'wthirdbar_r', 'wfifteenbar_r', 'resdept_r', 'drainagecl']

    extracted_access_tables_src_dir = os.path.abspath(SAMPLES_DIR)
    extracted_access_tables_src_dir_list = glob(f"{extracted_access_tables_src_dir}/*_summary.xlsx")

    for dir_ in extracted_access_tables_src_dir_list:
        df_major_components = extract_soil_inputs_from_tables(task=TASK_NO, data_input_dir=dir_)
        df_maj_comp_bkp = df_major_components.copy()

        df_major_components.apply(
            lambda row: create_store_file(
                row,
                cols_oi=task5_columns,
                ros_list_oi=ros_list_oi,
                rosfpath_list_oi=rosfpath_list_oi,
                df_maj_comp_bkp=df_maj_comp_bkp
            ),
            axis=1
        )
        # break

