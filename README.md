# sleeper-cli


Script for retrieving data through the Sleeper API. Set up right now to download all your league's rosters and output to a csv file that can be easily imported into a spreadsheet program, e.g. LibreOffice or Google Sheets. 

You might find it convenient for making a quick visible spreadsheet to share with the league, especially to manually set backups in case of sudden COVID game cancellations.  

Running the script with -h or --help will give you the command line options. 

-r to download the master player list from Sleeper (must be done at least once, should not be done more than once per day or they might cut off your access)

-l to pass a league number

-m to pass the maximum roster size in your league

-s to save your league number and max roster size locally. You can then call the script without extra arguments if you just need an updated sheet for your league

