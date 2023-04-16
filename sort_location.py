#!/usr/bin/env python

import os
import logging
from argparse import ArgumentParser
from pandas import read_csv
from geopy.geocoders import Nominatim
import folium

# --------------------------------------------------------------------------- #
# main routine
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    #-------- Parameters
    parser = ArgumentParser(description='Tools script to sort address on a map.')
    parser.add_argument("-d", "--data", help="CSV file holding all address.", default='liste_addr.csv')
    parser.add_argument("-p", "--path", help="Path to find file. Default is current directory", default=current_dir)
    parser.add_argument("-o", "--output", help="Path where to save output map. Default is current directory.", default=current_dir)
    parser.add_argument('-v', '--verbose', help='Add debug infos.', action='store_true')
    args = parser.parse_args()

    #-------- Debug set-up
    if(args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    #-------- File set-up
    data_file = os.path.abspath(os.path.join(args.path, args.data))
    output_file = os.path.abspath(os.path.join(args.path, 'map.html'))

    #-------- Parse data and add location
    data = read_csv(data_file)
    geolocator = Nominatim(user_agent="med_location")

    data['location'] = data['address'].apply(geolocator.geocode)
    data['point'] = data['location'].apply(lambda loc: tuple(loc.point) if loc else None)

    #-------- Create map
    m = folium.Map(location=[data['point'][0][0], data['point'][0][1]], zoom_start=12)

    for i in range(len(data)):
        folium.Marker([data['point'][i][0], data['point'][i][1]], popup=data['Name'][i]).add_to(m)

    m.save(output_file)