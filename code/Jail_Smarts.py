# Name: Mike Turtora
# Program: Jail_Smarts.py
# Decription: Script will pull data from Jail Population text files and hit
# SmartyStreets API for Address cleanup


"""
Watch the encoding!
https://smartystreets.com/docs/us-street-api
A common mistake we see is a non-encoded pound sign (#) like in an apartment
number (# 409). This character, when properly encoded in a URL, becomes %23.

A POST request allows a larger volume of data (MAX: 100 addresses or 32K per request)
to be sent in the HTTP Request Body. In this case, the data should be encoded as a
JSON array where each element in the array is a JSON object with field names
identical to those in the field listing below. Here's a sample request with two
addresses being sent...
"""
# Version: 0.1

import csv
import json
import pprint
import urllib
import pandas as pd
import sqlalchemy as sa

engine = sa.create_engine('sqlite:///jailpop.db')

# Array that holds the all the sliced out blocks
entry_blocks = []

# Dict keys for inmate data
inmate_table = {
    'SOID': '',
    'DOB': '',
    'Race': '',
    'Ethnicity': '',
    'Sex': '',
    'Address': '',
    'City': '',
    'POB': ''}

# dict keys for arrest data
arrest_table = {
    'BookingNum': '',
    'ArrestDate': '',
    'BookingDate': '',
    'ReleaseDate': '',
    'ReleaseCode': '',
    'RelRemarks': '',
    'ABN': '',
    'SOID': '',
    'Agency': ''}

# Initialize charge dict
charge_table = {}

# use Smarty Streets to normalize addresses
def read_auth():
    print 'READ AUTH'
    lines =[]
    with open('../data/SS.txt') as auth:
        lines = list(auth)
    auth_id = lines[3].rstrip()
    auth_token = lines[4].rstrip()
    return [auth_id, auth_token]


def get_smart(address_list):
    # Lookup address using SmartyStreets API
    # modeled after:
    # https://github.com/smartystreets/LiveAddressSamples/blob/master/python/street-address.py
    print 'GET_SMART'
    auth_list = read_auth()
    location = 'https://api.smartystreets.com/street-address'
    #location = 'https://api.smartystreets.com/lookup'
    query_string = urllib.urlencode({
    "auth-id": auth_list[0],
    "auth-token": auth_list[1],
    "street": address_list[0],
    "city": address_list[1],
    "state": address_list[2]
    })
    # what is this for: candidates=10'

    url = location + "?" + query_string
    print url

    response = urllib.urlopen(url).read()
    structure = json.loads(response)
    pprint.pprint(structure)

"""
    # error checking example for robustness
    creative_success = True
    try:
        clThings.raise_for_status()
        print "Tried"
    except requests.exceptions.HTTPError as e:
        creative_success = False
        print
        print "##### HANDLED EXCEPTION #####"
        print "cltampa.com error = ", e

    # Only have cl content to process if request succeeded
    if creative_success:
"""

def reverse_date(date_in):
    month = date_in[0:2]
    day = date_in[3:5]
    year = date_in[6:10]
    return year + '/' + month + '/' + day

def build_charge_table(book_num, charge_list, line_split, charge_count):
    charge_table['BookingNum'] = book_num
    charge_table['Charge_Type'] = line_split[1]
    charge_table['Charge'] = line_split[2]
    charge_table['CourtCode'] = line_split[3]
    charge_table['CourtCase'] = line_split[4]
    charge_list.append(charge_table.copy())
    # print "Charge List After line Two = ", charge_list


# Slices the data from Layout B into individual entries and stores them in entry_blocks
# But layout a not really used here...
def read_layout_b():
    """
    Reads a layout B file
    :return: entry_blocks - nested list representation of file
    """

    # Placeholder for blocks being sliced from file
    current_block = []

    # Read a layout b file into memory before processing.
    with open('..\\data\\LAYOUT B FILES\\samplecsv.csv') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')  #\t')
        for line in file_reader:
            #print line  # line is a 1 element list of type string.
            # a "block" is a record (multi-line data for one booking)
            # a booking ends with SOID so that is used to identify the end.
            current_block.append(line)
            for field in line:
                if 'SOID' in field:
                    entry_blocks.append(current_block)
                    current_block = []
    return entry_blocks

def parse_layout_b(entry_blocks):

    # Enters data from an entry in entry_blocks to table dictionaries
    # Creates a list of dicts for charges since they are many-to-one
    # Still need to check for empty charge dict (blank middle rows).

    #start_entry = True
    for entry in entry_blocks:
        # if start_entry:
        #     print 'Entry = ', entry
        #     start_entry = False
        # Need a charge list to support multiple charges per booking.
        # A list of dicts? Initialize here so it refreshes for each booking.
        charge_list = []
        charge_count = 0

        #start_list = True
        for line_list in entry:
            # if start_list:
            #     print 'line_list = ', line_list
            #     start_list = False

            # All first lines of an entry have the same format. This pulls the
            # data based on that format.
            #print "entry[0] =", entry[0]
            #print "entry[1] =", entry[1]
            #print "entry[2] =", entry[2]
            #print "entry[3] =", entry[3]

            if line_list == entry[0]:
                # first entry should be last name, first name, ...
                book_num = line_list[1]  # need to add book_num to other tables (rows)
                arrest_table['BookingNum'] = book_num
                arrest_table['Agency'] = line_list[4]
                arrest_table['ABN'] = line_list[5]

            # All second lines of an entry have the same format.
            # might need to check for missing values somewhere: write tests?
            elif line_list == entry[1]:
                #print "Second line in entry = ", line
                inmate_table['Race'] = line_list[0][0]
                inmate_table['Sex'] = line_list[0][4]
                inmate_table['Ethnicity'] = line_list[0][8]
                inmate_table['DOB'] = reverse_date(line_list[0][12:22])
                #print "inmate_table = ", inmate_table

            # Figure out how to properly check that charges aren't repeated. (maybe later)
            # Count attribute is in charge_table for multiples of same charge.
            # ?Make tempCharge list to hold them, check against held charge,
            # aggregate for counts?
                charge_count += 1
                build_charge_table(book_num, charge_list, line_list, charge_count)

            elif 'ADDRESS' in line_list[0]:
                # Handles formatting so the title for Address and POB aren't included.
                ##print "ADDRESS in line, line_list = ", line_list

                inmate_table['Address'] = line_list[0][line_list[0].find(':')+2:].strip()
                inmate_table['City'] = line_list[1].strip()
                inmate_table['POB'] = line_list[2][line_list[2].find(':')+2:].strip()

                # output addresses to file (temporary?)

                if inmate_table['Address']:
                    if inmate_table['City'] == 'TPA':
                        inmate_table['City'] = 'TAMPA'
                    if inmate_table['City'] == 'ST PETE':
                        inmate_table['City'] = 'ST PETERSBURG'

                    #print "Booking Number = ", book_num  # arrest_table['BookingNum']
                    #print inmate_table['Address'] + ', ' + inmate_table['City'] + ', FL'

                    address_string = inmate_table['Address'] + ', ' + inmate_table['City'] \
                        + ', FL' + '\n'

                    #OUTPUT.write(address_string)


            # SOID is always in last line of an entry. This pulls the data based on
            # that format.
            elif 'SOID' in line_list[2]:
                #print "SOID in line, line_list = ", line_list
                # Handles formatting so the title for ReleaseDate, ReleaseCode, and
                # SOID aren't included.
                arrest_table['ReleaseDate'] = reverse_date(line_list[0][line_list[0].find(':')+2:])
                arrest_table['ReleaseCode'] = line_list[1][line_list[1].find(':')+2:]
                arrest_table['SOID'] = line_list[2][line_list[2].find(':')+2:]
                inmate_table['SOID'] = line_list[2][line_list[2].find(':')+2:]

            else:
                # Finally, if not 1st, 2nd, or last, must be charge or blank
                ##print "Middle charge line, line_list = ", line_list
                # Test for blank before adding to dict
                empty = True
                #for field in line_list:
                for field in line_list:
                    if field.replace(' ', '').replace(',', ''):
                        empty = False
                if not empty:
                    charge_count += 1
                    build_charge_table(book_num, charge_list, line_list, charge_count)

        arrest_table['Counts'] = charge_count
        print "inmate_table = ", inmate_table
        print "arrest_table = ", arrest_table  #['Counts']
        print "charge_list = ", charge_list
        #print "Charge List In Else = ", charge_list

        # print "inmate_table = ", inmate_table
        # print "arrest_table = ", arrest_table
        # print "charge_list = ", charge_list

if __name__ == '__main__':

    print 'MAIN'
    entry_blocks = read_layout_b()
    parse_layout_b(entry_blocks)
    #with open('..\\data\\address.txt', 'w') as OUTPUT:


    address = ['7800 NEBRASKA AV N',
               'TAMPA',
               'FL']
    # Possible address test cases:
    #  SALVATION ARMY, TAMPA, FL
    #  BULL ROAD, DADE CITY, FL
    #get_smart(address)



