# Download from [Copernicus](http://marine.copernicus.eu)
This project aims to help with downloading oceanography data from the Copernicus.

## Why to bother?
The main goal of this project is to make downloading data straight forward by overcoming the naming conventions of Copernicus. The requests are sent in parallel and a NetCDF file is created per day.

## Installation
* In order to use this software - one has to have a Copernicus account ([create one here](http://marine.copernicus.eu/services-portfolio/register-now/))
* Make sure you have Python 2.7 installed (yes, that's very unfortunate but the motu client doesn't support Python 3).
* Install the [motu client](https://github.com/clstoulouse/motu-client-python):
```bash
pip install motu-client
```
* Add your Copernicus credentials to your environment variables:
```bash
export COPERNICUSUSERNAME <your copernicus username>
export COPERNICUSPASSWORD <your copernicus password>
```

## Running
Edit the config.py as you need, and the:
```bash
python download_from_copernicus.py
```

