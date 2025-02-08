import shutil
from urllib.request import urlretrieve
import os
import datetime
import urllib.request
import sys
import datetime
import pandas as pd
import os
import time
import logging
import subprocess
import pandas as pd
from pathlib import Path
from glob import glob
from urllib.error import URLError
from cigsatbuf_utils.envs import (
    DMWEA_EXEC,
    DMSOILP_EXEC
)
from cigsatbuf_utils.cig_tool_functions import adjust_sin_file

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
STA: int = 123456  # Station number (must be a 6-digit number)
NHR: int = 4  # Hours to distribute daily rain
BEGHR: int = 17  # Beginning hour

# Define the columns expected in the input CSV
COLS_OI = ["year", "yday", "tmax (deg c)", "tmin (deg c)", "prcp (mm/day)"]
NEW_COLS_OI = ["year", "yday", "tmax", "tmin", "prcp"]

def extract_location_properties(infile):
    output = { "period": [], "position": [], "location": "", "error": "", }

    try:
        with open(infile, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue  # Skip empty or commented lines
                try:
                    param, vals = map(str.strip, line.split(":", 1))  # Split only once
                    vals = [v.strip() for v in vals.split(",")]

                    if param == "period":
                        output["period"] = list(map(int, vals))
                    elif param == "position":  # Fixing the duplicate key issue
                        output["position"] = list(map(float, vals))
                    elif param == "location":
                        output["location"] = vals[0] if vals else ""
                except (ValueError, IndexError) as e:
                    output["error"] += f"Invalid line format: '{line}' - {e}\n"
    except FileNotFoundError:
        output["error"] = f"Error: File '{infile}' not found."
    except IOError as e:
        output["error"] = f"Error reading file '{infile}': {e}"

    return output

def daymet_timeseries(
    lat: float,
    lon: float,
    start_year: int,
    end_year: int,
    output_dir: str,
    prefix: str = ""
) -> str:
    """
    Download a Daymet timeseries for a single location as a local CSV file.

    Parameters:
        lat (float): Latitude of the location (within Daymet extent).
        lon (float): Longitude of the location (within Daymet extent).
        start_year (int): Start year (>= 1980).
        end_year (int): End year (< current year).
        output_dir (str): Directory to save the file.
        prefix (str, optional): Optional prefix for the filename. Defaults to "".

    Returns:
        str: Path to the downloaded CSV file.

    Raises:
        ValueError: If the requested data is outside Daymet coverage or the output directory is invalid.
        RuntimeError: If the request fails.
    """
    from urllib.error import URLError

    if not os.path.exists(output_dir):
        raise ValueError(f"Output directory '{output_dir}' does not exist.")

    max_year: int = datetime.datetime.now().year - 1
    start_year = max(start_year, 1980)
    end_year = min(end_year, max_year)

    year_range: str = ",".join(str(i) for i in range(start_year, end_year + 1))

    timeseries_url: str = (
        f"https://daymet.ornl.gov/data/send/saveData?"
        f"lat={lat}&lon={lon}&measuredParams=tmax,tmin,dayl,prcp,srad,swe,vp&"
        f"year={year_range}"
    )

    daymet_file: str = os.path.join(
        output_dir, f"{prefix}_Daymet_{lat}_{lon}_{start_year}_{end_year}.csv"
    )

    if os.path.exists(daymet_file):
        return daymet_file

    try:
        # Download the file
        urllib.request.urlretrieve(timeseries_url, daymet_file)

        # Check file size and remove if empty
        if os.path.exists(daymet_file) and os.path.getsize(daymet_file) == 0:
            os.remove(daymet_file)
            raise ValueError("Requested data is outside DAYMET coverage. Check coordinates!")

        return daymet_file

    except URLError as e:
        raise RuntimeError(f"Failed to download data: {e}")

def convert_degC_to_degF(temp_value: float) -> float:
    """Converts temperature from Celsius to Fahrenheit."""
    return 32 + (temp_value * 9 / 5)

def is_leap_year(year: int) -> bool:
    """Check if a given year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def insert_feb29(df: pd.DataFrame) -> pd.DataFrame:
    """Insert February 29 for leap years by averaging adjacent days' temperatures."""
    df = df.sort_values(['year', 'yday']).reset_index(drop=True)
    df_list = []

    for year in df['year'].unique():
        df_year = df[df['year'] == year].copy()

        if is_leap_year(year):
            df_before = df_year[df_year['yday'] < 60]
            df_after = df_year[df_year['yday'] >= 60].copy()
            df_after['yday'] += 1

            try:
                tmax_prev, tmax_next = df_year.loc[df_year['yday'] == 59, 'tmax'].values[0], df_year.loc[df_year['yday'] == 60, 'tmax'].values[0]
                tmin_prev, tmin_next = df_year.loc[df_year['yday'] == 59, 'tmin'].values[0], df_year.loc[df_year['yday'] == 60, 'tmin'].values[0]
            except IndexError:
                raise ValueError(f"Year {year} lacks necessary yday=59 or 60 data.")

            feb29_row = pd.DataFrame({'year': [year], 'yday': [60], 'tmax': [(tmax_prev + tmax_next) / 2], 'tmin': [(tmin_prev + tmin_next) / 2], 'prcp': [0]})
            df_year_modified = pd.concat([df_before, feb29_row, df_after], ignore_index=True)
        else:
            df_year_modified = df_year.copy()

        df_list.append(df_year_modified)

    return pd.concat(df_list, ignore_index=True).sort_values(['year', 'yday']).reset_index(drop=True)

def create_wea_files(df: pd.DataFrame, output_fpath: Path) -> tuple[Path, Path]:
    """Create .WEA files for temperature and precipitation."""

    rai_fpath = output_fpath.parent / f"{output_fpath.stem}_RAI.WEA"
    tem_fpath = output_fpath.parent / f"{output_fpath.stem}_TEM.WEA"

    if rai_fpath.exists() :
        raise FileExistsError(f"Output file {rai_fpath} already exist. Please delete it first.")
    if tem_fpath.exists():
        raise FileExistsError(f"Output file {tem_fpath} already exist. Please delete it first.")

    def format_value_str(value, temp=False):
        # The template .WEA file prefers .12 over 0.12
        nspaces = 6 if temp else 4
        nfrac = 1 if temp else 2
        npad = 8 if temp else 7
        if str(value)[0] == '0':
            value_str = format(value, f'.{nfrac}f')
            return nspaces * " " + value_str[1:4]
        else:
            return format(value, f'-{npad}.{nfrac}f')

    rai_wea_lines = []
    tem_wea_lines = []

    for i, row in df.iterrows():
        tmax_str = format_value_str(row["tmax"], temp=True)
        tmin_str = format_value_str(row["tmin"], temp=True)
        tem_line = format(row["year"], '-8n') + " " + format(row["yday"], '-7n') + tmax_str + tmin_str + "\n"
        rai_line = format(row["year"], '-4n') + " " + format(row["yday"], '-4n') + format_value_str(row["prcp"]) + "\n"

        tem_wea_lines.append(tem_line)
        rai_wea_lines.append(rai_line)


    with rai_fpath.open('w') as f:
        f.writelines(rai_wea_lines)
    with tem_fpath.open('w') as f:
        f.writelines(tem_wea_lines)

    return rai_fpath, tem_fpath

def run_dmwe_exec(file_path: Path, param_type: str, param_unit: str, ext: str):
    """Executes DMWEA program to process weather data."""
    cmd = f"{DMWEA_EXEC} {file_path} {param_type} {param_unit} {STA} {NHR} {BEGHR}"
    # logging.info(f"Executing: {cmd}")

    if subprocess.call(cmd, stderr=subprocess.DEVNULL) != 0:
        logging.error(f"Error running DMWEA for {file_path}")
        return

    log_files = list(file_path.parent.glob("*.log"))
    if not log_files:
        logging.warning(f"No log file found for {file_path}")
        return

    log_file = log_files[0]
    old_name = file_path.with_suffix(ext)
    new_name = old_name.with_name(old_name.name.replace("_RAI", "").replace("_TEM", ""))

    log_file.unlink()
    # old_name.unlink()
    return new_name

def from_daymet_weather_data_to_wea_files(input_fpath: Path, output_dir: Path):
    """Convert Daymet weather CSV to WEA files and run DMWEA."""
    df = pd.read_csv(input_fpath, skiprows=6, usecols=COLS_OI).rename(columns=dict(zip(COLS_OI, NEW_COLS_OI)))
    df["tmax"] = df["tmax"].apply(convert_degC_to_degF)
    df["tmin"] = df["tmin"].apply(convert_degC_to_degF)

    df = insert_feb29(df)

    output_fpath = output_dir / f"{'_'.join(input_fpath.stem.split('_')[:2])}.WEA"
    rai_fpath, tem_fpath = create_wea_files(df, output_fpath)

    rai_outfile = run_dmwe_exec(rai_fpath, "DR", "MM", ".RAI")
    tem_outfile = run_dmwe_exec(tem_fpath, "TP", "DF", ".TEM")

    return rai_outfile, tem_outfile


def run_dmsoilp_exec(file_path):
    

    # Run the program
    run_cmd = f"{DMSOILP_EXEC} {file_path}"
    output = subprocess.call(run_cmd, stderr=subprocess.DEVNULL)

    # Create file paths variables
    this_ros_file = file_path.split("\\")[-1][:-4]
    this_ros_dir = "\\".join(file_path.split("\\")[:-1])

    sin_file = this_ros_dir + f"\\{this_ros_file}.SIN"
    sin_file_bkp = sin_file.replace(".SIN", "_bkp.SIN")

    mis_file = this_ros_dir + f"\\{this_ros_file}.MIS"
    mis_file_bkp = mis_file.replace(".MIS", "_bkp.MIS")

    shutil.copy(sin_file, sin_file_bkp)
    shutil.copy(mis_file, mis_file_bkp)

    adjust_sin_file(sin_file=sin_file_bkp, output_SIN_file=sin_file, threshold_depth=90)
    os.remove(sin_file_bkp)
    os.remove(mis_file_bkp)

    this_ros_dir_files = glob(this_ros_dir + "\\*")

    # Check if .SIN and .MIS files are present
    print(f"{this_ros_file}:")
    if sin_file in this_ros_dir_files:
        print(f"\t - {this_ros_file}.SIN successfully created for {this_ros_file}")
    else:
        print(f"\t - No .SIN file created for {this_ros_file}")

    if mis_file in this_ros_dir_files:
        print(f"\t - {this_ros_file}.MIS successfully created for {this_ros_file}")
    else:
        print(f"\t - No .MIS file created for {this_ros_file}")
