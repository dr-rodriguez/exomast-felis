# Script for bulk load of old exomast JSON files


JSON_PATH = ""  # path to folder with JSON files

# Establish DB connection
# TODO: Write helper Class that inherits from astrodbKit.astrodb.Database

# TODO: Helper function to check existence of references first (move to method later)

# Loop over all JSON files

# Convert JSON data into dictionaries for insert
# Sources dict
# Coords dict
# Names dict
# Publications dict (which check for existence first)
# Porperties dict (only a few or all?)
# PlanetProperties dict (just orbital_period)

# Insert to DB
# TODO: check for duplicates? 
# TODO: handle updates?

# NO matching of Sources to happen yet
