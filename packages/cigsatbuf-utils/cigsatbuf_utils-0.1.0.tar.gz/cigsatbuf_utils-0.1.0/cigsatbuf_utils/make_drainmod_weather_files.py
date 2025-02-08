import os
import argparse
import logging
from pathlib import Path

from cigsatbuf_utils.helpers import (
    extract_location_properties,
    daymet_timeseries,
    from_daymet_weather_data_to_wea_files,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def download_daymet_weather_data(location_input_file, output_dir):
    """
    Download Daymet weather data for multiple locations specified in an input file.

    Parameters:
        location_input_file (str): Path to the input file containing location details.
        output_dir (str): Directory to save the downloaded files.

    Returns:
        Path: a path to the downloaded CSV files.
    """

    if not os.path.exists(location_input_file):
        raise FileNotFoundError(f"Input file '{location_input_file}' not found.")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    location_properties = extract_location_properties(location_input_file)
    if location_properties["error"]:
        raise ValueError(location_properties["error"])

    lat, lon = location_properties["position"]
    start_year, end_year = location_properties["period"]
    location_name = location_properties["location"]

    try:
        downloaded_file = daymet_timeseries(
            lat=lat,
            lon=lon,
            start_year=start_year,
            end_year=end_year,
            output_dir=output_dir,
            prefix=location_name
        )
        return Path(downloaded_file)
    except Exception as e:
        raise RuntimeError(f"Error downloading data for {location_name}: {e}")

def main(input_file: Path = None, output_dir: Path = None):
    """
    Main function to process Daymet weather data.

    Parameters:
        input_file (Path, optional): Path to the input file. If None, it will use CLI arguments.
        output_dir (Path, optional): Directory to save output. If None, it will use CLI arguments.
    """

    if isinstance(input_file, str):
        input_file = Path(input_file)
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    if input_file is None or output_dir is None:
        # Parse CLI arguments only if function is called without parameters
        parser = argparse.ArgumentParser(description="Download and convert Daymet weather data to WEA format.")
        parser.add_argument("-i", "--input", type=Path, required=True,
                            help="Path to the input file containing location details.")
        parser.add_argument("-o", "--output", type=Path, required=True, help="Directory to save the output files.")
        args = parser.parse_args()
        input_file, output_dir = args.input, args.output

    try:
        logging.info("Start downloading weather data...")
        timeseries_file_path = download_daymet_weather_data(input_file, output_dir)
        logging.info("Finished downloading weather data.")

        logging.info("Converting weather data to DRAINMOD's WEA files...")
        rai_outfile, tem_outfile = from_daymet_weather_data_to_wea_files(timeseries_file_path, output_dir)

        if rai_outfile and tem_outfile:
            logging.info("Finished converting weather data to WEA, RAI, and TEM files.")
            logging.info(f"All the output files are saved in the `{output_dir}` folder!")

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    fin = r".\samples\daymet_single_location_inputs.txt"
    output_dir = os.path.dirname(fin)
    fin = Path(fin)
    output_dir = Path(output_dir)

    main(fin, output_dir)