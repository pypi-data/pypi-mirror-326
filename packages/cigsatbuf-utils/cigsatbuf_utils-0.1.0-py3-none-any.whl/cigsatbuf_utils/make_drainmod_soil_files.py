
import os
import argparse
import logging
from glob import glob
from pathlib import Path

from cigsatbuf_utils.envs import ROSETTA_DIR
from cigsatbuf_utils.rosetta3 import Rpredict
from cigsatbuf_utils.retrieve_soil_components import extract_soil_inputs
from cigsatbuf_utils.helpers import run_dmsoilp_exec
from cigsatbuf_utils.helpers_gen_file import make_gen_file
from cigsatbuf_utils.helpers_store_file import extract_soil_inputs_from_tables, create_store_file, combine_all_store_files

logging.basicConfig(level=logging.INFO)

def create_ros_file(ssurgo_tabular_file, output_folder):
    
    if not os.path.exists(output_folder):
        raise FileNotFoundError(f"Output folder {output_folder} does not exist. Please create it first.")

    Rpredict.run(ssurgo_tabular_file, output_folder, rosetta_dir=ROSETTA_DIR)

    ros_files_match = os.path.join(output_folder, "*",  "*.ros")
    ros_files_list = glob(f"{ros_files_match}")

    if len(ros_files_list) == 0:
        print("No .ros file found or created. \nAborting...")
    return ros_files_list

def create_mis_and_sin_files(ros_files_list):
    
    if len(ros_files_list) == 0:
        print("No .ros file found or created. Must run create_ros_file.py first. Aborting...")
        return

    n_files = len(ros_files_list)
    for cnt, ros_fpath in enumerate(ros_files_list, 1):
        try:
            run_dmsoilp_exec(ros_fpath)
            print(f"\t*Finished creating MIS and SIN files for {ros_fpath} ({cnt}/{n_files})")
        except Exception as e:
            continue

def create_gen_files(ssurgo_tabular_file, ros_files_list, gen_file_template=None):
    if len(ros_files_list) == 0:
        print("No .SIN/.MIS file found or created. Must run create_ros_file.py first. Aborting...")
        return
    n_files = len(ros_files_list)
    for cnt, ros_fpath in enumerate(ros_files_list, 1):
        try:
            gen_fpath = ros_fpath.replace(".ros", ".gen")
            if os.path.exists(gen_fpath):
                print(f"Skipping {gen_fpath} as the file already exists")
                continue
            make_gen_file(ssurgo_tabular_file, gen_fpath, gen_file_template)
            print(f"\t*Finished creating {gen_fpath} ({cnt}/{n_files})")

        except Exception as e:
            print(f"Error happened: {e}. Skipping...\n")
            continue


def make_store_files(ssurgo_tables_dir, ros_files_list):

    ros_list_oi = [os.path.basename(ros_fpath).replace(".ros", "") for ros_fpath in ros_files_list]
    task5_columns = ['hzdepb_r', 'sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'ksat_r', 'wsatiated_r',
                     'wthirdbar_r', 'wfifteenbar_r', 'resdept_r', 'drainagecl']
    task_to_do = '5'

    df_major_components = extract_soil_inputs_from_tables(task_to_do, ssurgo_tables_dir)
    df_maj_comp_bkp = df_major_components.copy()

    df_major_components.apply(
        lambda row: create_store_file(
            row,
            cols_oi=task5_columns,
            ros_list_oi=ros_list_oi,
            rosfpath_list_oi=ros_files_list,
            df_maj_comp_bkp=df_maj_comp_bkp
        ),
        axis=1
    )


def combine_ssurgo_tables_into_one(ssurgo_tables_dir, output_folder=None):
    output_folder = os.path.abspath(output_folder) if output_folder else ssurgo_tables_dir

    dir_basename = os.path.basename(ssurgo_tables_dir)
    summary_fpath = os.path.join(output_folder, f"{dir_basename}_summary.xlsx")
    print(f"Processing the SSURGO tables from {ssurgo_tables_dir}")
    output_df, output_fpath = extract_soil_inputs(access_db_dir=ssurgo_tables_dir, output_fpath=summary_fpath, source='excel')
    return output_fpath


def main(ssurgo_tables_dir: Path = None, output_folder: Path = None, state_county: str = "state_county", gen_file_template: Path = None):
    """
    Main function to process SSURGO data.

    Parameters:
        ssurgo_tables_dir (Path, optional): Path to the SSURGO tables directory.
        output_folder (Path, optional): Directory to save the output files.
        gen_file_template (Path, optional): Optional template for generating .gen files.
    """

    if isinstance(ssurgo_tables_dir, str):
        ssurgo_tables_dir = Path(ssurgo_tables_dir)
    if isinstance(output_folder, str):
        output_folder = Path(output_folder)
    if isinstance(gen_file_template, str):
        gen_file_template = Path(gen_file_template)

    if ssurgo_tables_dir is None or output_folder is None:
        parser = argparse.ArgumentParser(description="Process SSURGO data and generate necessary output files.")
        parser.add_argument("-i", "--input", type=Path, required=True, help="Path to the SSURGO tables directory.")
        parser.add_argument("-o", "--output", type=Path, required=True, help="Directory to save the output files.")
        parser.add_argument("-s", "--state_county", type=Path, required=True, help="A name for the state and county. For example `IA_Benton`.") 
        parser.add_argument("-g", "--gen_template", type=Path, required=False, help="Optional path to .gen file template.")
        args = parser.parse_args()
        
        ssurgo_tables_dir, output_folder, state_county, gen_file_template = args.input, args.output, args.state_county, args.gen_template

    try:
        ssurgo_tabular_file = combine_ssurgo_tables_into_one(ssurgo_tables_dir, output_folder)

        ros_files_list = create_ros_file(ssurgo_tabular_file, output_folder)
        logging.info("****** Finished creating ROS files. ******")

        create_mis_and_sin_files(ros_files_list)
        logging.info("****** Finished creating MIS and SIN files. ******")

        create_gen_files(ssurgo_tabular_file, ros_files_list, gen_file_template)
        logging.info("****** Finished creating GEN files. ******")

        make_store_files(ssurgo_tables_dir, ros_files_list)
        logging.info("****** Finished creating STORE files. ******")

        combine_all_store_files(output_folder, state_county)

        logging.info("All tasks completed successfully.")

    except Exception as e:
        logging.error(f"Error: {e}")
        logging.error("Aborting...")


if __name__ == '__main__':
    main()