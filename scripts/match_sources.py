# Script to identify matching sources

import sqlalchemy as sa
from itertools import permutations
from astrodbkit.astrodb import Database
from config import CONNECTION_STRING, REFERENCE_TABLES, SCHEMA_NAME

THRESHOLD = 1.e-5  # period matching threshold
VERBOSE = False
DRYRUN = False  # do not do DB inserts

# Helper functions
def extract_tic(name_list: list):
    """Helper function to extract the TIC ID from a list of names."""

    for name in name_list:
        if name.startswith("TIC"):
            tic = name.split()[1] # split by spaces and get the TIC ID
            return tic

    return None


def match_by_name(db: Database, name_list: list, verbose: bool=False):
    """Match database sources using names. Returns a list of possible IDs"""

    # Identify matches by name
    t = db.query(db.Names.c.id).filter(db.Names.c.name.in_(name_list)).distinct().table()
    id_list = t["id"].tolist()
    if verbose:
        print(f"IDs matched by names: {id_list}")
    
    return id_list


def match_by_period(db: Database, tic: int, period: float, verbose: bool=False, threshold: float=1.e-5):
    """Match database sources using period and TIC ID. Returns a list of possible IDs"""
    
    # Break if no period is available for use or no TIC was provided
    if period is None or tic is None:
        return []

    # Fetch all IDs from toi/tess-dv that match the tic id
    t = db.query(db.Sources.c.id, db.Names.c.name, db.Sources.c.survey)\
            .join(db.Names, db.Sources.c.id == db.Names.c.id)\
            .filter(sa.and_(db.Sources.c.survey.in_(["toi", "TESS-DV"]),
                            db.Names.c.name.like(f"TIC {tic} %")))\
            .table()
    
    # Check if any matches
    if len(t) == 0:
        if verbose:
            print(f"No matches for TIC {tic}")
        return []
    else:
        if verbose:
            print(f"Entries from TOI/TESS-DV that match TIC {tic}")
            print(t)
    
    potential_ids = t["id"].tolist()

    # Filter down IDs by orbital period matching
    t = db.query(db.PlanetProperties.c.id, 
                db.PlanetProperties.c.orbital_period, 
                db.PlanetProperties.c.orbital_period_error,
                sa.label("diff", db.PlanetProperties.c.orbital_period - period))\
            .filter(sa.and_(db.PlanetProperties.c.id.in_(potential_ids),
                            db.PlanetProperties.c.orbital_period - period < threshold))\
            .table()
    if len(t) == 0:
        if verbose:
            print(f"No matches for TIC {tic} and period {period}")
        return []
    else:
        if verbose:
            print(f"Entries from TOI/TESS-DV that match TIC {tic} and have period close to {period}")
            print(t)
        potential_ids = t["id"].tolist()

    return potential_ids


def store_matches(db: Database, id_list: list, verbose: bool=False, dryrun: bool=True):
    """Function to handle storing all permutations of the matches for a single planet"""

    match_data = []
    
    # Check if match is already present, if so: skip
    for i, j in permutations(id_list, 2):  # 2 specifies pairs
        counts = db.query(db.Matches).filter(sa.and_(db.Matches.c.id1==i, db.Matches.c.id2==j)).count()
        if counts == 0:
            pair = {"id1": i, "id2": j}
            match_data.append(pair)

    if len(match_data) > 0 and not dryrun:
        # Actual ingest of data
        with db.engine.connect() as conn:
            conn.execute(db.Matches.insert().values(match_data))
            conn.commit()
        if verbose:
            print("Matched IDs stored in database")
    elif len(match_data) == 0 and not dryrun and verbose:
        print("No matches needed to be stored")
    elif dryrun and verbose:
        print(f"Dry-run is set, nothing loaded. These are the matched pairs: {match_data}")

    return


def run_match(db: Database, id: int, verbose: bool=False, dryrun: bool=True, threshold: float=1.e-5):
    """Wrapper function- will run all steps in the matching script for a given ID"""

    id_list = []

    # Identify matches by name
    # ========================

    # Fetch all the names for that ID
    t = db.query(db.Names.c.name).filter(db.Names.c.id==id).table()
    name_list = t["name"].tolist()

    # If this planet has names, use them for matching
    if len(name_list) > 0:
        if verbose:
            print(f"List of names for id {id}: {name_list}")
        name_matched_id = match_by_name(db, name_list, verbose=verbose)
    else:
        name_matched_id = []


    # Identify matches by TESS ID and orbital_period
    # ==============================================

    # Fetch orbital period
    t = db.query(db.PlanetProperties.c.id, 
                db.PlanetProperties.c.orbital_period, 
                db.PlanetProperties.c.orbital_period_error)\
        .filter(db.PlanetProperties.c.id==id).table()
    period = t["orbital_period"][0]
    # period_error = t["orbital_period_error"][0]

    # Get TIC ID from the name list
    tic = extract_tic(name_list)

    # Will return an empty list if TIC or period are missing
    period_match_id = match_by_period(db, tic=tic, period=period, verbose=verbose, threshold=threshold)


    # Verify matches
    # ==============

    # Combine match lists and remove any duplicates
    id_list = name_matched_id + period_match_id
    id_list = list(set(id_list))
    id_list.sort()

    # Query to check results
    t = db.query(db.Sources.c.id, db.Sources.c.survey, db.Sources.c.primary_name, 
                db.Coords.c.ra, db.Coords.c.dec,
                db.PlanetProperties.c.orbital_period, 
                db.PlanetProperties.c.orbital_period_error,)\
            .join(db.Coords, db.Sources.c.id == db.Coords.c.id)\
            .join(db.PlanetProperties, db.Sources.c.id == db.PlanetProperties.c.id)\
            .filter(db.Sources.c.id.in_(id_list))\
            .order_by(db.Sources.c.id)\
            .table()
    print(f"Final list of matches for ID {id}")
    print(t)

    # Store matches in match table
    # ============================

    store_matches(db, id_list, verbose=verbose, dryrun=dryrun)

    return


# ====================================================================================

# Actual script
db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema=SCHEMA_NAME)

id = 135  # HAT-P-11 b

# Loop over all sources and run their matches
t = db.query(db.Sources.c.id).table()
for id in t["id"].tolist():
    print(id)
    run_match(db=db, id=id, verbose=VERBOSE, dryrun=DRYRUN, threshold=THRESHOLD)
