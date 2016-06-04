# Name: Jessica Mack
# Program: JailSort.py
# Decription: Script will pull data from Jail Population Excel sheets and
# enter it into a MySQL database
# Version: 1.3

import csv

# import mysqldb

# Array that holds the all the sliced out blocks
entry_blocks = []

# List of charge_types. Used to verify that a line is a charge entry since the
# number of charges varies.
# MT: ?? Why do it this way? TEST: if not first, second, or last, must be charge?
charge_types = [
    'Probable Cause',
    'Capias',
    'Viol of Probation',
    'Warrant',
    'Court Order',
    'On Scene',
    'Direct Info',
    'Writ of Prosequend',
    'Order to Transport',
    'Viol of Parole',
    'Writ of Habeas Cor',
    'Recommit',
    'Removed From File']

# Holds the data for Inmate table in MYSQL db
# MT: try removing enclosing brackets to turn list into a dict
inmate_table = {
    'SOID': '',
    'DOB': '',
    'Race': '',
    'Ethnicity': '',
    'Sex': '',
    'Address': '',
    'City': '',
    'POB': ''}

# Holds data for the Arrest table in the MySQL db
# MT removed brackets
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

# Holds data for the CourtCase table in the MySQL db
# MT remove brackets

courtcase_table = {
    'CaseNum': '',
    'CourtCode': '',
    'SOID': '',
    'BookingNum': ''}

# Holds data for the Charge table in the MySQL db
charge_table = {
    'CaseNum': '',
    'CourtCode': '',
    'SOID': '',
    'Type': '',
    'Desc': '',
    'Counts': ''
}


# Slices the data from LayoutB into individual entries and stores them in entry_blocks
def block_maker(layout_a):
    file = open(layout_a)

    # Open database connection
    # db = mysqldb.connect('localhost','testuser','test','JailPop')

    # Placeholder for blocks being sliced from file
    current_block = []

    # Finds the end of an entry by slicing the file on the line with SOID
    # Adds the entry to entry_blocks for later disection
    with open('..\\data\\LAYOUT B FILES\\samplecsv.csv') as csvfile:
        filer_reader = csv.reader(csvfile, delimiter='\t')
        for line in filer_reader:
            # print line  # line is a 1 element list of type string.
            current_block.append(line)
            if 'SOID' in line[0]:  #str(line):
                entry_blocks.append(current_block)
                # print "Current Block = ", current_block  # a list of lists with 1 string
                current_block = []

    # Enters data from an entry in entry_blocks to table dictionaries
    for entry in entry_blocks:

        for line_list in entry:
            line = line_list[0]  #.pop()  #str(line_list)  # str(line)
            line_split = line.split(',')
            # All first lines of an entry have the same format. This pulls the
            # data based on that format.
            #print "entry[0] =", entry[0]
            #print "entry[1] =", entry[1]
            #print "entry[2] =", entry[2]
            #print "entry[3] =", entry[3]

            if line_list == entry[0]:
                # first entry should be last, first...
                #print "First line in entry = ", line
                #print "line_split = ", line_split
                for x in line_split:
                    # This is where I run into the issue with the index being a string
                    inmate_table['SOID'] = line_split[2]
                    # arrest_table['Agency'] = line[5]
                    # arrest_table['ABN'] = line[6]

            # All second lines of an entry have the same format. This pulls the
            # data based on that format.
            if line_list == entry[1]:
                print "Second line in entry = ", line
                inmate_table['Race'] = line_split[0][0]
                inmate_table['Sex'] = line_split[0][4]
                inmate_table['Ethnicity'] = line_split[0][8]
                inmate_table['DOB'] = line_split[0][12:21]
                print "inmate_table = ", inmate_table
            # Figure out how to properly check that charges aren't repeated.
            # Count attribute is in charge_table for multiples of same charge.
            # ?Make tempCharge list to hold them, check against held charge,
            # aggregate for counts?
            # charge_table['Type'] = line[6]
            # charge_table['Desc'] = line[7]
            # charge_table['Court'] = line[8]
            # charge_table['CaseNum'] = line[9]

            # This should find the lines that are only charge entries, if they exist.
            # This should skip the second line of an entry even though it has a
            # charge type.
            # if any(charge in charge_types for line in entry[x > 1]):
            # line = str(line)
            # line = line.split(',')
            # charge_table['Type'] = line[1]
            # charge_table['Desc'] = line[2]
            # charge_table['Court'] = line[3]
            # charge_table['CaseNum'] = line[4]

            # ADDRESS will always be in second to last line of an entry. This pulls the
            # data based on that format.

            """

            if 'ADDRESS' in line:
                line = str(line)
                line = line.split(',')
                # Handles formatting so the title for Address and POB aren't included.
                line = line.split(':')
                inmate_table['Address'] = line[1]
                inmate_table['City'] = line[2]
                inmate_table['POB'] = line[4]

            # SOID is always in last line of an entry. This pulls the data based on
            # that format.
            if 'SOID' in str(line):
                line = str(line)
                line = line.split(',')
                # Handles formatting so the title for ReleaseDate, ReleaseCode, and
                # SOID aren't included.
                line = line.split(':')
                # arrest_table['ReleaseDate'] = line[1]
                # arrest_table['ReleaseCode'] = line[3]
                inmate_table['SOID'] = line[5]

            """


            # Will take the data from the dictionaries and enter them into the
                # JailPop database
            # Still need to work out a looping feature to execute the queries
            # Also, need to include a checking feature that will ensure there aren't
                # redundant entries

            # cursor = db.cursor()

            # SQL queries to INSERT a record into the database.
            # queries = (inmateSql, arrestSql, courtcaseSql, chargeSql)

            # Some values will be repeated. They can just be set equal to each other.
            # inmateSql = """INSERT INTO INMATE(SOID, DOB, RACE, ETHNICITY, SEX, ADDRESS, CITY, POB)
            # VALUES (inmate_table['SOID'], inmate_table['DOB'], inmate_table['Race'], inmate_table['Ethnicity'],
            # inmate_table['Sex'], inmate_table['Address'], inmate_table['City'], inmate_table['POB']) """
            # arrestSql = """INSERT INTO ARREST(BOOKINGNUM, ARRESTDATE, BOOKDATE, RELEASEDATE, RELEASECODE, RELREMARKS, ABN, SOID, AGENCY)
            # VALUES (arrest_table['BookingNum'], arrest_table['ArrestDate'], arrest_table['BookingDate'], arrest_table['ReleaseDate'],
            # arrest_table['ReleaseCode'], arrest_table['RelRemarks'], arrest_table['ABN'], arrest_table['SOID'], arrest_table['Agency'])"""
            # courtcaseSql = """INSERT INTO COURTCASE(CASENUM, COURTCODE, SOID, BOOKINGNUM)
            # VALUES (courtcase_table['CaseNum'], courtcase_table['CourtCode'], courtcase_table['SOID'], courtcase_table['BookingNum'])"""
            # chargeSql = """INSERT INTO CHARGE(CASENUM, COURTCODE, SOID, TYPE, DESC, COUNTS)
            # VALUES (charge_table['CaseNum'], charge_table['CourtCode'], charge_table['SOID'], charge_table['Type'], charge_table['Desc'], charge_table['Counts'])"""

            # try:
            # cursor.execute( _ ) > Change to loop through the queries above
            # db.commit()
            # except:
            # Rollback in case there is any error
            # db.rollback()

    # db.close()
    file.close()


block_maker('..\data\LAYOUT A FILES\\1 LAYOUT A CSV.csv')
