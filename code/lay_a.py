from os import listdir
import csv

'''
arrest_table = {
    'BookingNum': '',
    'ArrestDate': '',
    'BookingDate': '', ?
    'ReleaseDate': '',
    'ReleaseCode': '',
    'RelRemarks': '', ?
    'ABN': '',
    'SOID': '',
    'Agency': ''}
'''

# following has only non-redundant fields and key
arrest_table = {
    'BookingNum': '',
    'BookingDate': '',
    'RelRemarks': ''}


if __name__ == "__main__":
    dir_list = listdir("..\\data\\LAYOUT A FILES")
    print dir_list
    for filename in dir_list:
        with open("..\\data\\LAYOUT A FILES" + '\\' + filename) as lay_ay:
            file = csv.reader(lay_ay, delimiter=',', quotechar='"')
            for line in file:
                arrest_table['BookingNum'] = line[0]
                arrest_table['BookingDate'] = line[6]
                arrest_table['RelRemarks'] = line[9]
        print arrest_table



