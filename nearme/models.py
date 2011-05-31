#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nearme geospatial referencing
# https://github.com/heynemann/nearme

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from mongoengine import *

class Place(Document):
    name = StringField(max_length=255, required=True)
    ascii_name = StringField(max_length=255, required=True)
    alternate_names = ListField(StringField(max_length=255))
    region = StringField(max_length=255)
    country_code = StringField(max_length=20)
    population = IntField()
    elevation = FloatField()
    timezone = StringField()
    point = GeoPointField()

    meta = {
        'indexes': [
            'point'
        ]
    }

    #return {
        #'geonameid': values[0],
        #'name': values[1],
        #'ascii_name': values[2],
        #'alternate_names': values[3].split(','),
        #'latitude': float(values[4]),
        #'longitude': float(values[5]),
        #'feature_class': values[6],
        #'feature_code': values[7],
        #'country_code': values[8],
        #'cc2': values[9].split(','),
        #'admin1': values[10],
        #'admin2': values[11],
        #'admin3': values[12],
        #'admin4': values[13],
        #'population': values[14],
        #'elevation': values[15],
        #'gtopo30': values[16],
        #'timezone': values[17],
        #'mod_date': values[18]
    #}

    @classmethod
    def from_values(cls, values):
        item = cls(
            name=values['name'],
            ascii_name=values['ascii_name'],
            alternate_names=values['alternate_names'],
            region="Rio de Janeiro",
            country_code=values['country_code'],
            population=int(values['population']),
            timezone='',
            point=[float(values['latitude']), float(values['longitude'])]
        )

        if values['elevation']:
            item.elevation = float(values['elevation'])

        return item
