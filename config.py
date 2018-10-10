from regions import REGIONS

start_date = '2017-10-01'
end_date = '2018-03-31'

# possible variables:
# 'sea_surface_temperature', 'sea_surface_temperature_night',
# 'sea_surface_chlorophyll', 'sea_surface_velocities'

variables = ['sea_surface_velocities']
temporal = 'daily'
level = 'L3'
processing = 'REP'

region = 'MED'

if region:
    coordinates = REGIONS[region]
else:
    coordinates = {
        'lon': {
            'min': 30,
            'max': 38
        },
        'lat': {
            'min': 24,
            'max': 36
        }
    }

lon, lat = coordinates['lon'], coordinates['lat']

output_directory = 'data'
