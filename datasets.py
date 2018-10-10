services = {
    'daily': {
        'MED': {
            'CHL': {
                'L3': {
                    'NRT': {
                        'id': 'OCEANCOLOUR_MED_CHL_L3_NRT_OBSERVATIONS_009_040-TDS',
                        'spatial_resolution': '1km',
                        },
                    'REP': {
                        'id': 'OCEANCOLOUR_MED_CHL_L3_REP_OBSERVATIONS_009_073-TDS',
                        'spatial_resolution': '1km',
                        },
                    }
                },
                'L4': {
                    'NRT': {
                        'id': 'OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041-TDS',
                        'spatial_resolution': '1km',
                        },
                    'REP': {
                        'id': 'OCEANCOLOUR_MED_CHL_L4_REP_OBSERVATIONS_009_078-TDS',
                        'spatial_resolution': '1km',
                    },
                },
            },
            'SST': {
                'L3': {
                    'NRT': {
                        'id': 'SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012-TDS',
                        'spatial_resolution': '0.063deg',
                        },
                },
            },
            'SSH': {
                'L4': {
                    'id': 'SEALEVEL_MED_PHY_L4_NRT_OBSERVATIONS_008_050-TDS',
                    'spatial_resolution': '0.125deg',
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
                    'NRT': {
                        'id': 'dataset-oc-med-chl-multi-l3-chl_1km_daily-rt-v02',
                        },
                    'REP': {
                        'id': 'dataset-oc-med-chl-multi_cci-l3-chl_1km_daily-rep-v02',
                        },
                    }
                },
                'L4': {
                    'NRT': {
                        'id': 'dataset-oc-med-chl-multi-l4-interp_1km_daily-rt-v02',
                        },
                    'REP': {
                        'id': ''
                    },
                }
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
    }
