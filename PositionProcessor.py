import os
import csv
from nmea.NMEAParser import NMEAParser

print('Windows utility to process NMEA 0183 v. 4.11 sentences for land survey/position only')
print('GGA is processed for XYZ positions')
print('RMC is processed for COG, SOG and date')
print('GST is processed for XYZ accuracy')
input('Press ENTER to continue...')

output_file_name = './processed/summary.csv'
print(f'Saving data as {output_file_name}')
# Now create the CSV file and headers
output_file = open(output_file_name, 'w', newline='')
with output_file:
    file_header = ['Longitude', 'Latitude', 'Altitude', 'SOG', 'CMG', 'Sigma Latitude', 'Sigma Longitude', 'Sigma Altitude', 'True Heading', 'Fix quality', 'Date', 'UTC']
    writer = csv.writer(output_file)
    writer.writerow(file_header)

# Raw data files
directory = './logfiles'

# Instantiate an object to parse NMEA
myNMEA = NMEAParser()

# Open every file in sequence
for file in os.listdir(directory):
    input_filename = directory + '/' + file
    print("Found" + input_filename)
    # Process each file individually
    with open(input_filename) as nmea_file:
        # one line at a time, parse
        for CurrentNMEAString in nmea_file:
            # Check for a garbled string
            if CurrentNMEAString.isascii():
                myNMEA.parser(CurrentNMEAString)
                if myNMEA.gga_valid and myNMEA.rmc_valid and myNMEA.gst_valid:
                    output_file = open(output_file_name, 'a', newline='')
                    with output_file:
                        line_data = [myNMEA.dd_longitude_degrees,
                                     myNMEA.dd_latitude_degrees, myNMEA.altitude, myNMEA.sog, myNMEA.cmg,
                                     myNMEA.sigma_latitude, myNMEA.sigma_longitude, myNMEA.sigma_altitude,
                                     myNMEA.heading_true, myNMEA.fix_quality, myNMEA.date_of_fix, myNMEA.gps_time]
                        writer = csv.writer(output_file)
                        writer.writerow(line_data)

                        # Wait until valid GGA, RMC and GST before saving in CSV again.
                        myNMEA.gga_valid = False
                        myNMEA.rmc_valid = False
                        myNMEA.gst_valid = False