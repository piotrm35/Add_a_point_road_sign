# -*- coding: utf-8 -*-

class Setup:
    
    WIDTH = 7
    HEIGHT = 7
    START_DATE = '2019-02-11T11:19'
    COMMENTS = ''

    COMMENTS_MAX_LENGTH = 100
    DB_FIELD_NAMES_MAPPING_DICT = {
        'ROAD_SIGN_TYPE': 'type',
        'ANGLE': 'angle',
        'WIDTH': 'width',
        'HEIGHT': 'height',
        'START_DATE': 'start',
        'COMMENTS': 'comments'
        }
    MANUAL_FILE_NAME = 'APRS_manual_EN.pdf'
