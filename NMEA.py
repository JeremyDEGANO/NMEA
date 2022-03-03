from pickletools import long1
import sys
import os
import pandas as pd
import pynmea2
import datetime
import folium
from branca.element import Figure

data = {'date':[],'lat':[], 'long':[], 'alt':[]}
file = ""

def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))
    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)

def read_nmea(file,data):
    file = open(file, "r")
    for line in file:
        if str(line).startswith("$GPGGA"):
            nmeaobj = pynmea2.parse(line)
            ['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) 
            for i in range(len(nmeaobj.fields))]
            data['alt'].append(nmeaobj.altitude)
        if str(line).startswith("$GPRMC"):
            nmeaobj = pynmea2.parse(line)
            ['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) 
            for i in range(len(nmeaobj.fields))]
            datestamp = str(nmeaobj.datestamp) + '' + str(nmeaobj.timestamp)
            data['date'].append(datestamp)
            data['lat'].append(nmeaobj.latitude)
            data['long'].append(nmeaobj.longitude)
    dataframe = pd.DataFrame.from_dict(data)
    file.close()
    return dataframe
data = read_nmea(file, data)
fmap = folium.Map(tiles='OpenStreetMap', zoom_start=8)
for i in range(len(data)):
    folium.Marker(location=[data['lat'].iloc[i], data['long'].iloc[i]]).add_to(fmap)
data.to_xml('nmea.xml')
fmap.save('via.html')
