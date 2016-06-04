# Name: Jessica Mack
# Program: JailSort.py
# Decription: Script will pull data from Jail Population Excel sheets and enter it into a MySQL database
# Version: 1.3

import csv
#import mysqldb

# Array that holds the all the sliced out blocks
entryBlocks = []

# List of chargeTypes. Used to verify that a line is a charge entry since the number of charges varies.
chargeTypes = [
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
inmateTable = [{
	'SOID': '',
	'DOB': '',
	'Race': '',
	'Ethnicity': '',
	'Sex': '',
	'Address': '',
	'City': '',
	'POB': ''}]

# Holds data for the Arrest table in the MySQL db
arrestTable = [{
	'BookingNum': '',
	'ArrestDate': '',
	'BookingDate': '',
	'ReleaseDate': '',
	'ReleaseCode': '',
	'RelRemarks': '',
	'ABN': '',
	'SOID': '',
	'Agency': ''}]

# Holds data for the CourtCase table in the MySQL db	
courtcaseTable = [{
	'CaseNum': '',
	'CourtCode': '',
	'SOID': '',
	'BookingNum': ''}]

# Holds data for the Charge table in the MySQL db
chargeTable = [{
	'CaseNum': '',
	'CourtCode': '',
	'SOID': '',
	'Type': '',
	'Desc': '',
	'Counts': ''
	}]

# Slices the data from LayoutB into individual entries and stores them in entryBlocks
def blockMaker(file):
	file = open(file)
	
	# Open database connection
	#db = mysqldb.connect('localhost','testuser','test','JailPop')
	
	# Placeholder for blocks being sliced from file
	currentBlock = []
	
	# Finds the end of an entry by slicing the file on the line with SOID
	# Adds the entry to entryBlocks for later disection
	with open('..\\data\\LAYOUT B FILES\\samplecsv.csv') as csvfile:
		filereader = csv.reader(csvfile, delimiter='\t')
		for line in filereader:
			currentBlock.append(line)
			if 'SOID' in str(line):
				entryBlocks.append(currentBlock)
				currentBlock = []		
	
	# Enters data from an entry in entryBlocks to table dictionaries
	for entry in entryBlocks:
		for line in entry:
			# All first lines of an entry have the same format. This pulls the data based on that format.
			if line == entry[0]:
				line = str(line)
				line = line.split(',')
				for x in line:
					inmateTable['SOID'] = line[2] # This is where I run into the issue with the index being a string
					#arrestTable['Agency'] = line[5]
					#arrestTable['ABN'] = line[6]
						
			# All second lines of an entry have the same format. This pulls the data based on that format.
			if line == entry[1]:
				line = str(line)
				line = line.split(',')
				slash = '/'
				line = line.split(slash)
				inmateTable['Race'] = line[0]
				inmateTable['Sex'] = line[1]
				inmateTable['Ethnicity'] = line[2]
				inmateTable['DOB'] = slash.join(line[5], line[3], line[4])
			# Figure out how to properly check that charges aren't repeated. 
			# Count attribute is in chargeTable for multiples of same charge.
			# ?Make tempCharge list to hold them, check against held charge, aggregate for counts?
				#chargeTable['Type'] = line[6]
				#chargeTable['Desc'] = line[7]
				#chargeTable['Court'] = line[8]
				#chargeTable['CaseNum'] = line[9]
					
			# This should find the lines that are only charge entries, if they exist.
			# This should skip the second line of an entry even though it has a charge type.
			#if any(charge in chargeTypes for line in entry[x > 1]):
				#line = str(line)
				#line = line.split(',')
				#chargeTable['Type'] = line[1]
				#chargeTable['Desc'] = line[2]
				#chargeTable['Court'] = line[3]
				#chargeTable['CaseNum'] = line[4]
			
			# ADDRESS will always be in second to last line of an entry. This pulls the data based on that format.
			if 'ADDRESS' in line:
				line = str(line)
				line = line.split(',')
				# Handles formatting so the title for Address and POB aren't included.
				line = line.split(':')
				inmateTable['Address'] = line[1]
				inmateTable['City'] = line[2]
				inmateTable['POB'] = line[4]
			
			# SOID is always in last line of an entry. This pulls the data based on that format.
			if 'SOID' in str(line):
				line = str(line)
				line = line.split(',')
				# Handles formatting so the title for ReleaseDate, ReleaseCode, and SOID aren't included.
				line = line.split(':')
				# arrestTable['ReleaseDate'] = line[1]
				# arrestTable['ReleaseCode'] = line[3]
				inmateTable['SOID'] = line[5]
			
		# Will take the data from the dictionaries and enter them into the JailPop database
		# Still need to work out a looping feature to execute the queries
		# Also, need to include a checking feature that will ensure there aren't redundant entries
		
			# cursor = db.cursor()

			# SQL queries to INSERT a record into the database.
			# queries = (inmateSql, arrestSql, courtcaseSql, chargeSql)
			
			# Some values will be repeated. They can just be set equal to each other.
			# inmateSql = """INSERT INTO INMATE(SOID, DOB, RACE, ETHNICITY, SEX, ADDRESS, CITY, POB)
							# VALUES (inmateTable['SOID'], inmateTable['DOB'], inmateTable['Race'], inmateTable['Ethnicity'], 
							# inmateTable['Sex'], inmateTable['Address'], inmateTable['City'], inmateTable['POB']) """
			# arrestSql = """INSERT INTO ARREST(BOOKINGNUM, ARRESTDATE, BOOKDATE, RELEASEDATE, RELEASECODE, RELREMARKS, ABN, SOID, AGENCY)
							# VALUES (arrestTable['BookingNum'], arrestTable['ArrestDate'], arrestTable['BookingDate'], arrestTable['ReleaseDate'], 
							# arrestTable['ReleaseCode'], arrestTable['RelRemarks'], arrestTable['ABN'], arrestTable['SOID'], arrestTable['Agency'])"""
			# courtcaseSql = """INSERT INTO COURTCASE(CASENUM, COURTCODE, SOID, BOOKINGNUM)
							# VALUES (courtcaseTable['CaseNum'], courtcaseTable['CourtCode'], courtcaseTable['SOID'], courtcaseTable['BookingNum'])"""
			# chargeSql = """INSERT INTO CHARGE(CASENUM, COURTCODE, SOID, TYPE, DESC, COUNTS)
							# VALUES (chargeTable['CaseNum'], chargeTable['CourtCode'], chargeTable['SOID'], chargeTable['Type'], chargeTable['Desc'], chargeTable['Counts'])"""
	 
			# try:
			   # cursor.execute( _ ) > Change to loop through the queries above
			   # db.commit()
			# except:
			   # Rollback in case there is any error
			   # db.rollback()

	# db.close()
	file.close()

blockMaker('..\data\LAYOUT A FILES\\1 LAYOUT A CSV.csv')
