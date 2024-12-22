# Script to identify matching sources

from astrodbkit.astrodb import Database
from config import CONNECTION_STRING, REFERENCE_TABLES, SCHEMA_NAME

# Helper functions
def extract_tic(name_list: list):
    """Helper function to extract the TIC ID from a list of names."""

    for name in name_list:
        if name.startswith("TIC"):
            tic = name.split()[1] # split by spaces and get the TIC ID
            return tic

    return None


db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema=SCHEMA_NAME)


id = 5574
id_list = []

# Identify matches by name
# ========================

# Fetch all the names for that ID
t = db.query(db.Names.c.name).filter(db.Names.c.id==id).table()
name_list = t["name"].tolist()
print(name_list)

# Get TIC ID for later
tic = extract_tic(name_list)
print(tic)

# Identify matches by name
t = db.query(db.Names.c.id).filter(db.Names.c.name.in_(name_list)).distinct().table()
id_list += t["id"].tolist()
print(id_list)


# Identify matches by TESS ID and orbital_period
# ==============================================

# Fetch orbital period
# Fetch all IDs from toi/tess-dv that match the tic id
# Filter down IDs by orbital period matching (round to 2 digits)
# Append to initial id_list and remove any duplicates

# Store matches in match table
# ============================