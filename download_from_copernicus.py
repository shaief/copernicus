from concurrent.futures import ThreadPoolExecutor
import datetime
import os
import subprocess

from config import (
    start_date,
    end_date,
    variables,
    temporal,
    level,
    lon,
    lat,
    output_directory, )

from datasets import services, products
import get_region

try:
    COPERNICUSUSERNAME = os.environ['COPERNICUSUSERNAME']
    COPERNICUSPASSWORD = os.environ['COPERNICUSPASSWORD']
except KeyError:
    print(
        'Could not find Copernicus credentials. Please make sure you set the following:'
    )
    print('\t$ export COPERNICUSUSERNAME <your copernicus username>')
    print('\t$ export COPERNICUSPASSWORD <your copernicus password>')
    print(
        '\n\n if you are using virtualenv (highly recommended!) this can be done automatically in your \'activate\' file as follows:'
    )
    print('add these lines at the end of your file:')
    print('''
        \t# This hook runs after the virtual environment is activated.
        \texport COPERNICUSUSERNAME="USERNAME"
        \texport COPERNICUSPASSWORD="PASSWORD"

    ''')
    print('''
    If you would like to remove the credentials when leaving the virtualenv,
    add these lines at the 'deactivate' part of the file:
    ''')
    print('''
        \tunset COPERNICUSUSERNAME
        \tunset COPERNICUSPASSWORD
    ''')

MOTU = 'http://nrt.cmems-du.eu/motu-web/Motu'

if 'sea_surface_chlorophyll' in variables:
    product = 'CHL'
    day_night = 'D'
    variables.remove('sea_surface_chlorophyll')
    variables.extend(['CHL', 'WTM', 'SENSORMASK', 'QI'])
elif 'sea_surface_temperature_night' in variables:
    product = 'SST'
    day_night = 'N'
    variables.remove('sea_surface_temperature_night')
    variables.insert(0, 'sea_surface_temperature')
    variables.extend(['adjusted_sea_surface_temperature',
                      'source_of_sst', 'quality_level'])
elif 'sea_surface_velocities' in variables:
    product = 'SSH'
    day_night = 'D'
    level = 'L4'
    variables.remove('sea_surface_velocities')
    variables.extend(['sla', 'adt', 'ugos', 'vgos',
                      'ugosa', 'vgosa', 'err'])

region = get_region.from_coordinates(lon, lat)


def download(date):
    print('.')
    # request = '{}_{}_{}_{}'.format(product.upper(),
    #                                temporal.lower(),
    #                                spatial_resolution.lower(),
    #                                region.upper())

    # service_id = services[product][region][spatial_resolution][temporal][level]
    service = services[temporal][region][product][level]
    service_id = service['id']
    spatial_resolution = service['spatial_resolution']
    product_id = products[temporal][region][product][level]['id']
    # product_id = products[product][region][spatial_resolution][temporal][level]

    output_file = 'COP_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.nc'.format(
        level,
        product,
        day_night,
        spatial_resolution,
        temporal,
        lon['min'],
        lon['max'],
        lat['min'],
        lat['max'],
        date, )

    print(output_file)

    cmd_variables = []
    for variable in variables:
        cmd_variables.append('--variable')
        cmd_variables.append(variable)

    cmd = [
        'python', '-m', 'motu-client', '--user', COPERNICUSUSERNAME, '--pwd',
        COPERNICUSPASSWORD, '--motu', MOTU, '--service-id', service_id,
        '--product-id', product_id, '--longitude-min', str(lon['min']),
        '--longitude-max', str(lon['max']), '--latitude-min', str(lat['min']),
        '--latitude-max', str(lat['max']), '--date-min', date, '--date-max',
        date, '--out-dir', output_directory, '--out-name', output_file
    ]
    cmd.extend(cmd_variables)

    print(cmd)

    subprocess.call(cmd)


start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
delta = end - start
print(delta)
with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(delta.days + 1):
        date = start + datetime.timedelta(days=i)
        print(date)
        # download(str(date))
        future = executor.submit(download, str(date))
