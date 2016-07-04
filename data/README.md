# Notes on data folder contents
ab name and dob list 415431 names.xlsx : provided by Phil to Antonio for cross reference.

## Structure
Notes on the below should be completed over time.

Built w/ Win10 "tree /a /f > repo_structure.txt" then edited manually.

/jailpop...
  |   .gitattributes
  |   .gitignore
  |   auth.txt
  |   HCSO Records Request.odt
  |   HCSO Records Request.pdf
  |   links.txt
  |   mjt dij slice 2x2015 x ONLY ALL BOOKINGS DETAILS 43268 33018 HU'S 342 ETC .xlsx
  |   numbers.txt
  |   repo_structure.txt
  |   test_numbers.txt
  |   
  |       
  +---code
  |   |   JailSort_ver2.py - attempt to put LAYOUT files into mysql db.
  |   |                      need to merge in recent edits (in /postapalooza)
  |   |   lay_a.py
  |   |   send_text.py
  |   |   ...
  |   |   
  +---data
  |   |   ab name and dob list 415431 names.xlsx
  |   |   README.md
  |   |   
  |   +---LAYOUT A FILES (files created by Phil by copying from HCSO website)
  |   |       1 LAYOUT A CSV.csv
  |   |       2 LAYOUT A CSV.csv
  |   |       
  |   +---LAYOUT B FILES
  |   |       1 LAYOUT B CSV.csv
  |   |       2 LAYOUT B CSV.csv
  |   |         ...
  |   |       9 LAYOUT B CSV.csv
  |   |       samplecsv.csv
  |   |       
  |   +---Notes and Correspondence
  |   |       Email xchnge about excel list for xref 20160701.pdf
  |   |       
  |   +---Odyssey
  |   |       Odyssey-JobOutput-June 01, 2016 06-32-43-1609654-3.TXT
  |   |       Odyssey-Test Data.TXT
  |   |       
  |   \---sqlite
