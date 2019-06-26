from regions import REGIONS

start_date = '2018-07-10'
end_date = '2018-07-30'

# possible variables:
# 'sea_surface_temperature', 'sea_surface_temperature_night',
# 'sea_surface_chlorophyll', 'sea_surface_velocities'

# variables = ['sea_surface_velocities']
variables = ['sea_surface_chlorophyll']
temporal = 'daily'
level = 'L3'
processing = 'REP'

region = 'MED'

if region:
    coordinates = REGIONS[region]
else:
    coordinates = {
        # 'lon': {
        #     'min': 30,
        #     'max': 38
        # },
        # 'lat': {
        #     'min': 24,
        #     'max': 36
        # }
        # 8.4-8.9E / 41.4-41.9N
        # 'lon': {
        #     'min': 8.4,
        #     'max': 8.9
        # },
        # 'lat': {
        #     'min': 41.4,
        #     'max': 41.9
        # }
    }

lon, lat = coordinates['lon'], coordinates['lat']

output_directory = 'data'
