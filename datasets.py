services = {
    'daily': {
        'MED': {
            'CHL': {
                'L3': {
                    'id':
                    'OCEANCOLOUR_MED_CHL_L3_NRT_OBSERVATIONS_009_040-TDS',
                    'spatial_resolution': '1km',
                },
                'L4': {
                    'id': '',
                },
            },
            'SST': {
                'L3': {
                    'id': 'SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012-TDS',
                    'spatial_resolution': '0.063deg',
                },
            },
            'SSH': {
                'L4': {
                    'id': 'SEALEVEL_MED_PHY_L4_NRT_OBSERVATIONS_008_050-TDS',
                    'spatial_resolution': '0.125deg',
                },
            },
        },
    },
    '8days': {
        'MED': {
            'CHL': {
                'L4': {
                    'id':
                    'OCEANCOLOUR_MED_CHL_L3_NRT_OBSERVATIONS_009_040-TDS',
                    'spatial_resolution': '1km',
                },
            },
        },
    }
}

products = {
    'daily': {
        'MED': {
            'CHL': {
                'L3': {
                    'id': 'dataset-oc-med-chl-multi-l3-chl_1km_daily-rt-v02',
                },
            },
            'SST': {
                'L3': {
                    'id': 'SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012_a',
                },
            },
            'SSH': {
                'L4': {
                    'id': 'dataset-duacs-nrt-medsea-merged-allsat-phy-l4',
                },
            },
        },
    },
}
