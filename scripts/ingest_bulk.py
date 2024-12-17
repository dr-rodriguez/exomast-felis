# Script for bulk load of old exomast JSON files

import os
import json
from astrodbkit.astrodb import Database
from sqlalchemy import func

CONNECTION_STRING = "postgresql+psycopg://postgres:password@localhost:5432/exomast"
REFERENCE_TABLES = [
    "Publications",
    "Surveys",
]
JSON_PATH = "/Users/drodriguez/data/CF/exomast-catalog/data/output/exoplanetsOrg"  # path to folder with JSON files
FILE_LIMIT = 5

# TODO: Write helper Class that inherits from astrodbKit.astrodb.Database
# TODO: Assign incrementing ID by survey?

# TODO: Helper function to check existence of references first (move to method later)
def check_publication(db, bibcode: str = None, reference: str = None, verbose: bool = False):
    """
    Check Publications table for present of given bibcode/reference

    Parameters
    ----------
    bibcode
    reference
    verbose
    """

    present_in_db = False

    # Rely on bibcode first if provided
    if bibcode is not None and bibcode != "":
        t = db.query(db.Publications).filter(db.Publications.c.bibcode == bibcode).table()
    elif reference is not None and reference != "":
        t = db.query(db.Publications).filter(db.Publications.c.reference == reference).table()
    else:
        t = []

    # Potential match(es) found
    if len(t) == 1:
        present_in_db = True
        if verbose:
            print(f"Single match for {bibcode}/{reference}.")
            print(t)
    elif len(t) > 1:
        msg = f"More than one match for {bibcode}/{reference}: {len(t)}"
        print(msg)
        if verbose:
            print(t)
        raise RuntimeError(msg)

    return present_in_db


def fetch_next_id(db, survey=""):
    """
    Helper function to fetch the next available Source value for a given survey
    """

    # Get the largest ID
    t = db.query(func.max(db.Sources.c.id).label("max_id")).table()
    max_id = t["max_id"][0]

    if max_id is not None:
        max_id += 1
    else:
        max_id = 1

    return max_id


def extract_bibcode(url: str):
    """
    Helper function to extract bibcode from url

    Example URLs:
    http://adsabs.harvard.edu/abs/2010A%26ARv..18...67T
    https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
    """

    bibcode = None
    temp = None

    if url is not None and url != "":
        temp = url.split("/")[-1]

    # Handle URL cases
    if temp is not None and temp.endswith(".html"):
        bibcode = None
    else:
        bibcode = temp

    return bibcode


# Main code

# Establish DB connection
db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema="exomast")

# Loop over all JSON files
count = 0
for file in os.listdir(JSON_PATH):
    if not file.endswith(".json"):
        continue
    if count >= FILE_LIMIT:
        break

    # Load the JSON data
    filename = os.path.join(JSON_PATH, file)
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(count)
    print(data)

    # TODO: check for duplicates?
    # TODO: handle updates?

    # Get the next available Source id
    id = fetch_next_id(db, survey="")

    # Convert JSON data into dictionaries for insert

    # TODO: Publications dict (with check for existence first)
    # Not all references are real papers, may need to have some logic/exclude list

    # Sources dict
    source_data = [
        {
            "id": id,
            "source_type": "exoplanet",
            "survey": data.get("catalog_name"),
            "primary_name": data.get("planet_name"),
        },
    ]

    # Coords dict
    coords_data = [
        {
            "id": id,
            "ra": data.get("ra"),
            "dec": data.get("dec"),
        }
    ]

    # Names dict
    name_list = [data.get("planet_name")] + data.get("name_list", [])
    name_list = list(set(name_list))  # remove any duplicates
    names_data = [{"id": id, "name": n} for n in name_list]

    # TODO: Properties dict (only a few or all?)
    # TODO: PlanetProperties dict (just orbital_period)

    # Actual ingest of data
    with db.engine.connect() as conn:
        conn.execute(db.Sources.insert().values(source_data))
        conn.execute(db.Coords.insert().values(coords_data))
        conn.execute(db.Names.insert().values(names_data))
        conn.commit()

    count += 1

# NO matching of Sources to happen yet
