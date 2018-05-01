from collections import namedtuple

Region = namedtuple('Region', 'name lat lon')
regions = [
    Region(name='MED', lat=(30, 45.99854660342), lon=(-6, 36.500480651855)),
    Region(name='EUR', lat=(20, 70), lon=(-40, 55)),
]


def from_coordinates(lat, lon):
    if not lat['min'] < lat['max']:
        lat['min'], lat['max'] = lat['max'], lat['min']

    if not lon['min'] < lon['max']:
        lon['min'], lon['max'] = lon['max'], lon['min']

    for r in regions:
        if (r.lat[0] <= lat['min'] and lat['max'] <= r.lat[1]) and (
                r.lon[0] <= lon['min'] and lon['max'] <= r.lon[1]):
            return r.name
    else:
        print('Could not figure out the region from the supplied coordinates')
