#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))


from ivcap_df import Schema, RefColumn, Column, ColType, Connector

common_ns = 'common'
geo_location_s = Schema('geo_location', common_ns, 'The geographic coordinates of a place or event', [
    Column('elevation', ColType.FLOAT64, description="The elevation of a location (WGS 84). Value alone should be assumed to be in meters.", required=False),
    Column('latitude', ColType.FLOAT64, description="The latitude of a location. For example 37.42242 (WGS 84)."),
    Column('longitude', ColType.FLOAT64, description="The longitude of a location. For example -122.08585 (WGS 84)."),
])

geo_line_s = Schema('geo_line', common_ns, 'The geographic coordinates of a line defined by a from and to locations', [
    RefColumn('from', geo_location_s, description='Location of the beginning of the line'), 
    RefColumn('to', geo_location_s, description='Location of the end of the line'), 
])

image_s = Schema('image', common_ns, 'An image',  [
    Column('url', ColType.STRING, format='uri'),
    Column('description', ColType.STRING, required=False),
    Column('format', ColType.STRING, required=False),
    Column('width', ColType.INT64, description="Image width in pixels", unit='pixel', required=False),
    Column('height', ColType.INT64, description="Image height in pixels", unit='pixel', required=False),
    Column('taken_at', ColType.DATETIME64_NS_TZ, description='The date and time this image was taken (in ISO 8601 date format).', format='date-time', required=False),
    RefColumn('location', geo_location_s, required=False), 
])

collection_membership_s = Schema('in_collection', common_ns, 'Associates an artifact to a specific collection',  [
    RefColumn('collection', description='The URN of the collection'),
    RefColumn('artifact', description='The URN of the artifact in the collection'),
])

schemas = {
    'geo_location_s': geo_location_s,
    'geo_line_s': geo_line_s,
    'image': image_s,
    'in_collection': collection_membership_s,
}

print(Schema.to_dot(schemas.values(), fontSize=10))

ivcap_params = {"type": "ivcap"}
with Connector(**ivcap_params) as conn:
    for name, schema in schemas.items():
        print(name)
        schema.persist(conn, verbose=True)
print("...schema done")

 