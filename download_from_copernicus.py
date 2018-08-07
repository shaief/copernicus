#! venv/bin/python

import argparse
import ast
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import os
import subprocess

from tqdm import tqdm

from config import (
    start_date,
    end_date,
    variables,
    temporal,
    level,
    lon,
    lat,
    output_directory,
)
from datasets import services, products
import get_region

Input = namedtuple(
    "Input", ["dates", "variable", "level", "lons", "lats", "output_dir", "verbosity"]
)

try:
    COPERNICUSUSERNAME = os.environ["COPERNICUSUSERNAME"]
    COPERNICUSPASSWORD = os.environ["COPERNICUSPASSWORD"]
except KeyError:
    print(
        "Could not find Copernicus credentials. Please make sure you set the following:"
    )
    print("\t$ export COPERNICUSUSERNAME <your copernicus username>")
    print("\t$ export COPERNICUSPASSWORD <your copernicus password>")
    print(
        "\n\n if you are using virtualenv (highly recommended!) this can be done automatically in your 'activate' file as follows:"
    )
    print("add these lines at the end of your file:")
    print(
        """
        \t# This hook runs after the virtual environment is activated.
        \texport COPERNICUSUSERNAME="USERNAME"
        \texport COPERNICUSPASSWORD="PASSWORD"

    """
    )
    print(
        """
    If you would like to remove the credentials when leaving the virtualenv,
    add these lines at the 'deactivate' part of the file:
    """
    )
    print(
        """
        \tunset COPERNICUSUSERNAME
        \tunset COPERNICUSPASSWORD
    """
    )

MOTU = "http://nrt.cmems-du.eu/motu-web/Motu"


def organize_inputs(user_input):
    start = datetime.datetime.strptime(user_input.dates[0], "%Y-%m-%d").date()
    end = datetime.datetime.strptime(user_input.dates[1], "%Y-%m-%d").date()
    delta = end - start

    variables = user_input.variable
    if set.intersection({"sea_surface_chlorophyll", "chl"}, variables):
        product = "CHL"
        day_night = "D"
        if user_input.level == "L3":
            variables = ["CHL", "WTM", "SENSORMASK", "QI"]
        elif user_input.level == "L4":
            variables = ["CHL"]
    elif set.intersection({"sea_surface_temperature_night", "sst_night"}, variables):
        print("boooohooo")
        product = "SST"
        day_night = "N"
        variables = [
            "sea_surface_temperature",
            "adjusted_sea_surface_temperature",
            "source_of_sst",
            "quality_level",
        ]
    elif "sea_surface_velocities" in variables:
        product = "SSH"
        day_night = "D"
        level = "L4"
        variables = ["sla", "adt", "ugos", "vgos", "ugosa", "vgosa", "err"]
    else:
        raise ValueError("Missing variable")

    region = get_region.from_coordinates(lon, lat)
    return {
        "start": start,
        "delta": delta,
        "lons": user_input.lons,
        "lats": user_input.lats,
        "level": user_input.level,
        "temporal": temporal,
        "region": region,
        "product": product,
        "day_night": day_night,
        "variables": variables,
    }


def download(date, params, verbosity):
    region = params["region"]
    product = params["product"]
    variables = params["variables"]
    level = params["level"]
    day_night = params["day_night"]
    lon = params["lons"]
    lat = params["lats"]
    service = services[temporal][region][product][level]
    service_id = service["id"]
    spatial_resolution = service["spatial_resolution"]
    product_id = products[temporal][region][product][level]["id"]

    output_file = "COP_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.nc".format(
        level,
        product,
        day_night,
        spatial_resolution,
        temporal,
        lon[0],
        lon[1],
        lat[0],
        lat[1],
        date,
    )

    # print(output_file)

    cmd_variables = []
    for variable in variables:
        cmd_variables.append("--variable")
        cmd_variables.append(variable)

    cmd = [
        "python",
        "-m",
        "motu-client",
        "--user",
        COPERNICUSUSERNAME,
        "--pwd",
        COPERNICUSPASSWORD,
        "--motu",
        MOTU,
        "--service-id",
        service_id,
        "--product-id",
        product_id,
        "--longitude-min",
        str(lon[0]),
        "--longitude-max",
        str(lon[1]),
        "--latitude-min",
        str(lat[0]),
        "--latitude-max",
        str(lat[1]),
        "--date-min",
        date,
        "--date-max",
        date,
        "--out-dir",
        output_directory,
        "--out-name",
        output_file,
    ]
    if not verbosity:
        cmd.extend(["--quiet"])
    cmd.extend(cmd_variables)

    # print(cmd)

    subprocess.call(cmd)


def parse_user_input(lons, lats):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start", type=str, help="yyyy-mm-dd", nargs="?", default=start_date
    )
    parser.add_argument(
        "--end", type=str, help="yyyy-mm-dd", nargs="?", default=end_date
    )
    parser.add_argument(
        "--var", type=str, help="CHL/SST/SST_night", nargs="?", default=variables
    )
    # parser.add_argument("--temporal", type=str, help="daily", nargs='?', default=temporal)
    parser.add_argument("--level", type=str, help="L3/L4", nargs="?", default=level)
    parser.add_argument("--lon", type=str, help="[min, max]", nargs="?", default=lons)
    parser.add_argument("--lat", type=str, help="[min, max]", nargs="?", default=lats)
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory path",
        nargs="?",
        default=output_directory,
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        action="store_true",
        help="If used - prints out verbose information",
    )
    args = parser.parse_args()
    dates = args.start, args.end
    var = [args.var] if type(args.var) != list else args.var
    # temporal = args.temporal
    processing_level = args.level
    lons = ast.literal_eval(args.lon)
    lats = ast.literal_eval(args.lat)
    if not (type(lons) == list and type(lats) == list):
        print("Lat/Lon should be a list of this format: [min,max]")
    elif not (len(lons) == 2 and len(lats) == 2):
        print("Lat/Lon should be a list of this format: [min,max]")

    output_dir = args.output
    verbosity = args.verbosity
    return Input(dates, var, processing_level, lons, lats, output_dir, verbosity)


def main():
    lons = str([lon["min"], lon["max"]])
    lats = str([lat["min"], lat["max"]])

    user_input = parse_user_input(lons, lats)
    organized_inputs = organize_inputs(user_input)

    start = organized_inputs["start"]
    delta = organized_inputs["delta"]

    msg = """
    Downloading the following data:
    {} days between {} --> {} of {} {} data in the area of:
    Longitudes: {} --> {}
    Latitudes: {} --> {}
    to directory: {}
    """
    print(
        msg.format(
            delta.days + 1,
            user_input.dates[0],
            user_input.dates[1],
            user_input.variable,
            user_input.level,
            user_input.lons[0],
            user_input.lons[1],
            user_input.lats[0],
            user_input.lats[1],
            user_input.output_dir,
        )
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        for i in range(delta.days + 1):
            date = start + datetime.timedelta(days=i)
            future_list += [
                executor.submit(
                    download, str(date), organized_inputs, user_input.verbosity
                )
            ]
        for future_object in tqdm(as_completed(future_list), total=len(future_list)):
            future_object.result()


if __name__ == "__main__":
    main()
