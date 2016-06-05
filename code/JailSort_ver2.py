# Name: Jessica Mack
# Program: JailSort.py
# Decription: Script will pull data from Jail Population Excel sheets and
# enter it into a MySQL database
# Version: 1.3

import csv
import mysql.connector
from mysql.connector import Error


# Array that holds the all the sliced out blocks
entry_blocks = []

# List of charge_types. Used to verify that a line is a charge entry since the
# number of charges varies.
# MT: ?? Why do it this way? TEST: if not first, second, or last, must be charge?
# charge_types = [
    # 'Probable Cause',
    # 'Capias',
    # 'Viol of Probation',
    # 'Warrant',
    # 'Court Order',
    # 'On Scene',
    # 'Direct Info',
    # 'Writ of Prosequend',
    # 'Order to Transport',
    # 'Viol of Parole',
    # 'Writ of Habeas Cor',
    # 'Recommit',
    # 'Removed From File']

# Holds the data for Inmate table in MYSQL db
# MT: try removing enclosing brackets to turn list into a dict
# Will need to check for consistency since address could change (at the least)
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
	
charge_table = {}

# Holds data for the CourtCase table in the MySQL db
# MT remove brackets
# Not sure why SOID included here, Booking Number should be key
	#courtcase_table = {
    # 'CourtCase': '',
    # 'CourtCode': '',
    # 'SOID': '',
    # 'BookingNum': ''}

# Holds data for the Charge table in the MySQL db
# Not sure why SOID here, should be Booking Number?
# courtcase_table and charge_table redundant? courtcase obsolete?
# MT removed SOID, should just need booking number for key

def reverse_date(date_in):
	#line_split[0][12:22])
	month = date_in[0:2]
	day = date_in[3:5]
	year = date_in[6:10]
	return year + '/' + month + '/' + day
	

def build_charge_table(book_num, charge_list, line_split, charge_count):
    # added BookingNum to charge_table
    # need to append to dict to avoid overwrite
    print charge_count
    charge_table['Counts'] = charge_count
    charge_table['BookingNum'] = book_num
    charge_table['Charge_Type'] = line_split[1]
    charge_table['Charge'] = line_split[2]
    charge_table['CourtCode'] = line_split[3]
    charge_table['CourtCase'] = line_split[4]
    charge_list.append(charge_table.copy())
    # print "Charge List After line Two = ", charge_list


# Slices the data from LayoutB into individual entries and stores them in entry_blocks
def block_maker(layout_a):
    file = open(layout_a)

    # Placeholder for blocks being sliced from file
    current_block = []

    # Finds the end of an entry by slicing the file on the line with SOID
    # Adds the entry to entry_blocks for later disection
    with open('..\\data\\LAYOUT B FILES\\samplecsv.csv') as csvfile:
        filer_reader = csv.reader(csvfile, delimiter=',', quotechar='"')  #\t')
        #print filer_reader
        for line in filer_reader:
            #print line  # line is a 1 element list of type string.
            current_block.append(line)
            for field in line:
                if 'SOID' in field:  #line[0]:  #str(line):
                    entry_blocks.append(current_block)
                    # print "Current Block = ", current_block  # a list of lists with 1 string
                    current_block = []


    # Enters data from an entry in entry_blocks to table dictionaries

    # Creates a list of dicts for charges since they are many-to-one
    # Still need to check for empty charge dict (blank middle rows).

    for entry in entry_blocks:
        print
        #print 'Entry = ', entry
        # Need a charge list to support multiple charges per booking.
        # A list of dicts? Initialize here so it refreshes for each booking.
        charge_list = []
        charge_count = 0
		
        for line_list in entry:
            #print 'line_list = ', line_list
            line = line_list  #[0]  # extract string from one element list

            # if double quote need to remove embedded comma
            line_split = line  #.split(',')

            # All first lines of an entry have the same format. This pulls the
            # data based on that format.
            #print "entry[0] =", entry[0]
            #print "entry[1] =", entry[1]
            #print "entry[2] =", entry[2]
            #print "entry[3] =", entry[3]

            if line_list == entry[0]:
                # first entry should be last name, first name, ...
                # need to add names for consistency checks

                ##print
                ##print "First line in entry = ", line
                ##print "line_split = ", line_split

                book_num = line_split[1]  # need to add book_num to other tables (rows)
                arrest_table['BookingNum'] = book_num
                arrest_table['Agency'] = line_split[4]
                # why is ABN in charge_table since it's on first line?
                # will need to save it here to add it for other charge lines.
                arrest_table['ABN'] = line_split[5]

            # All second lines of an entry have the same format.
            # might need to check for missing values somewhere: write tests?
            elif line_list == entry[1]:
                ##print "Second line in entry = ", line
                inmate_table['Race'] = line_split[0][0]
                inmate_table['Sex'] = line_split[0][4]
                inmate_table['Ethnicity'] = line_split[0][8]
                inmate_table['DOB'] = reverse_date(line_split[0][12:22])
				##print "inmate_table = ", inmate_table

            # Figure out how to properly check that charges aren't repeated. (maybe later)
            # Count attribute is in charge_table for multiples of same charge.
            # ?Make tempCharge list to hold them, check against held charge,
            # aggregate for counts?
                charge_count += 1
                build_charge_table(book_num, charge_list, line_split, charge_count)

				
            elif 'ADDRESS' in line_list[0]:
                # Handles formatting so the title for Address and POB aren't included.
                #line = line.split(':')
                ##print "ADDRESS in line, line_split = ", line_split

                inmate_table['Address'] = line_split[0][line_split[0].find(':')+2:]
                inmate_table['City'] = line_split[1]
                inmate_table['POB'] = line_split[2][line_split[2].find(':')+2:]
                #print inmate_table


            # SOID is always in last line of an entry. This pulls the data based on
            # that format.
            elif 'SOID' in line_list[2]:
                #print "SOID in line, line_split = ", line_split
                # Handles formatting so the title for ReleaseDate, ReleaseCode, and
                # SOID aren't included.
                arrest_table['ReleaseDate'] = reverse_date(line_split[0][line_split[0].find(':')+2:])
                arrest_table['ReleaseCode'] = line_split[1][line_split[1].find(':')+2:]
                arrest_table['SOID'] = line_split[2][line_split[2].find(':')+2:]
                inmate_table['SOID'] = line_split[2][line_split[2].find(':')+2:]
				#print arrest_table
			
            else:
                # Finally, if not 1st, 2nd, or last, must be charge or blank
                ##print "Middle charge line, line_split = ", line_split
                # Test for blank before adding to dict
                empty = True
                for field in line_list:
                    if field.replace(' ', '').replace(',', ''):
                        empty = False
                if not empty:
                    charge_count += 1
                    build_charge_table(book_num, charge_list, line_split, charge_count)

					
            arrest_table['Counts'] = charge_count
                    #print "Charge List In Else = ", charge_list

        ##print "inmate_table = ", inmate_table
        ##print "arrest_table = ", arrest_table
        #print "charge_list = ", charge_list
		
		# Open database connection
	'''
		jailpopconnect = mysql.connector.connect(host='localhost',database='jailpop',user='testuser',password='test')
		cursor = jailpopconnect.cursor()
		
        # Will take the data from the dictionaries and enter them into the
        # JailPop database
        # Still need to work out a looping feature to execute the queries
        # Also, need to include a checking feature that will ensure there aren't
        # redundant entries

        # Some values will be repeated. They can just be set equal to each other.
		inmateSql = "INSERT INTO INMATE " \
					"(SOID, DOB, RACE, ETHNICITY, SEX, ADDRESS, CITY, POB) " \
					"VALUES ('" + inmate_table['SOID'] + "', '" + inmate_table['DOB'] + "', '" + inmate_table['Race'] + "', '" + inmate_table['Ethnicity'] + "', '" \
					+ inmate_table['Sex'] + "', '" + inmate_table['Address'] + "', '" + inmate_table['City'] + "', '" + inmate_table['POB'] + "')"
		#print inmateSql
				
		arrestSql = "INSERT INTO ARREST" \
					"(BOOKINGNUM, ARRESTDATE, BOOKDATE, RELEASEDATE, RELEASECODE, RELREMARKS, ABN, SOID, AGENCY)" \
					"VALUES ('" + arrest_table['BookingNum'] + "', '" + arrest_table['ArrestDate'] + "', '" + arrest_table['BookingDate'] + "', '" + arrest_table['ReleaseDate'], "', '" \
					+ arrest_table['ReleaseCode'] + "', '" + arrest_table['RelRemarks'] + "', '" + arrest_table['ABN'] "', '" + arrest_table['SOID'] + "', '" + arrest_table['Agency'] + "')"
				
		chargeSql = "INSERT INTO CHARGE" \
					"(CASENUM, COURTCODE, SOID, Charge_Type, DESC, COUNTS)" \
					"VALUES ('" + charge_table['CourtCase'] + "', '" + charge_table['CourtCode'] + "', '" + charge_table['SOID'] + "', '" \
					+ charge_table['Charge_Type'] + "', '" + charge_table['Charge'] + "', '" + charge_table['Counts'] + "')"
				
		# SQL queries to INSERT a record into the database.
		queries = (inmateSql, arrestSql, chargeSql)
				
		try:
			#Change to loop through the queries above
			for query in queries:
				cursor.execute(query) 
				jailpopconnect.commit()
			
		except Error as error:
            #Rollback in case there is any error
			jailpopconnect.rollback()
			print error

		cursor.close()
		jailpopconnect.close()
    file.close()
	'''



block_maker('..\data\LAYOUT A FILES\\1 LAYOUT A CSV.csv')
