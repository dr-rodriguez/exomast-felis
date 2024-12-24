# Script for bulk load of old exomast JSON files

import json
import os
import socket
from datetime import datetime

from astrodbkit.astrodb import Database
from config import CONNECTION_STRING, REFERENCE_TABLES, SCHEMA_NAME
from sqlalchemy import func, and_

# How many to process; set to 0 or less to do all
FILE_LIMIT = 0
VERBOSE = False
DRYRUN = False  # control whether to ingest or not

# Determine path of JSON files
machine_name = socket.gethostname()
if "maelstrom" in machine_name:
    ROOT_PATH = "/Users/drodriguez/data/CF/exomast-catalog/data/output/"
elif "Strakul" in machine_name:
    ROOT_PATH = "/Users/strakul/PycharmProjects/exomast-catalog/data/output/"
# path to folder with JSON files
# JSON_PATH = ROOT_PATH + "exoplanetsOrg"
JSON_PATH = ROOT_PATH + "nexsci"
# JSON_PATH = ROOT_PATH + "koi"
# JSON_PATH = ROOT_PATH + "toi"
# JSON_PATH = ROOT_PATH + "tess_dv"


# TODO: Write helper Class that inherits from astrodbKit.astrodb.Database
# TODO: Assign incrementing ID by survey?


def check_publication(
    db, bibcode: str = None, reference: str = None, verbose: bool = False
):
    """
    Check Publications table for present of given bibcode/reference.
    Return publication information if present.

    Parameters
    ----------
    bibcode
    reference
    verbose
    """

    # Rely on bibcode first if provided
    if bibcode is not None and bibcode != "":
        t = (
            db.query(db.Publications)
            .filter(db.Publications.c.bibcode == bibcode)
            .table()
        )
    elif reference is not None and reference != "":
        t = (
            db.query(db.Publications)
            .filter(db.Publications.c.reference == reference)
            .table()
        )
    else:
        t = []

    # Potential match(es) found
    if len(t) == 1:
        if verbose:
            print(f"Single match for {bibcode}/{reference}.")
            print(t)
    elif len(t) > 1:
        msg = f"More than one match for {bibcode}/{reference}: {len(t)}"
        print(msg)
        if verbose:
            print(t)
        raise RuntimeError(msg)

    return t


def fetch_next_source_id(db, survey=""):
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

    return int(max_id)


def fetch_next_publication_id(db):
    """
    Helper function to fetch the next available Publication ID
    """

    # Get the largest ID
    t = db.query(func.max(db.Publications.c.id).label("max_id")).table()
    max_id = t["max_id"][0]

    if max_id is not None:
        max_id += 1
    else:
        max_id = 1

    return int(max_id)


def extract_bibcode(url: str):
    """
    Helper function to extract bibcode from url

    Example URLs:
    http://adsabs.harvard.edu/abs/2010A%26ARv..18...67T
    https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
    """

    bibcode = None
    temp = None

    # Extract bib code from ADS url
    if url is not None and url != "":
        # Strip out any /abstract parts
        temp = url.replace("/abstract", "").split("/")[-1]

    # Handle HTML cases
    if temp is not None and (
        temp.endswith(".html") or temp.endswith(".php") or temp == ""
    ):
        bibcode = None
    else:
        bibcode = temp

    return bibcode


def extract_from_nested_json(data: dict, parameter: str, subparameter: str):
    """Helper function to extract information from nexted JSON.
    Example:
    "orbital_period": {
        "value": 265.59,
        "unit": "d",
        "uerror": 1.04,
        "lerror": 1.04,
        "reference": "Dalal et al. 2021"
    },
    """

    temp = data.get(parameter)
    value = None

    if temp is not None and isinstance(temp, dict):
        value = temp.get(subparameter)

    return value


def extract_all_urls(data):
    """
    This function recursively traverses the JSON data structure and extracts all keys named "url".
    AI-generated via Gemini 2.0 Flash

    Args:
        data: The JSON data structure (dictionary or list).

    Returns:
        A list of all "url" key values found in the data.
    """

    urls = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "url":
                urls.append(value)
            else:
                # Recursively call the function for nested dictionaries and lists
                urls.extend(extract_all_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_all_urls(item))

    return urls


def process_publications(db: Database, data: dict):
    """Logic to process all publications in a JSON file and return a mapping dictionary"""

    # Get all URLs in the JSON information
    all_urls = extract_all_urls(data)
    all_urls = list(set(all_urls))
    url_map = {}

    # Loop over each, extracting bibcode when possible
    for url in all_urls:
        if url is None:
            continue

        bibcode = extract_bibcode(url)
        reference = None

        if bibcode is None:
            # Attempt to use reference information from URL
            reference = url.replace(".html", "").split("/")[-1]
            if reference == "":
                reference = None
        # TODO: May need some better handling since some values are in reference and not url
        # Also, some cases are empty string and being handled improperly
        # Long-term this may be a moot point- the references may be handled directly from the
        # source material as opposed to extracing from the limited JSON information.

        # Check if in DB already
        t = check_publication(db=db, bibcode=bibcode, reference=reference)
        if len(t) == 0:
            pub_id = fetch_next_publication_id(db=db)
            # Add to database
            publication_data = [
                {"id": pub_id, "bibcode": bibcode, "reference": reference}
            ]
            with db.engine.connect() as conn:
                conn.execute(db.Publications.insert().values(publication_data))
                conn.commit()
        else:
            pub_id = int(t["id"][0])
        url_map[url] = pub_id

    return url_map


# =====================================================================================
# Main code

# Establish DB connection
db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema=SCHEMA_NAME)

start_time = datetime.now()

# Loop over all JSON files
count = 0
for file in os.listdir(JSON_PATH):
    if not file.endswith(".json"):
        continue
    if FILE_LIMIT > 0 and count >= FILE_LIMIT:
        break

    # Load the JSON data
    filename = os.path.join(JSON_PATH, file)
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if VERBOSE:
        print(count)
        print(data)

    # Check for duplicates by survey+primary_name+modification_date?
    survey = data.get("catalog_name")
    primary_name = data.get("planet_name")
    modification_date = datetime.fromisoformat(data.get("modification_date"))
    t = (
        db.query(db.Sources)
        .filter(
            and_(
                db.Sources.c.survey == survey,
                db.Sources.c.primary_name == primary_name,
                db.Sources.c.modification_date == modification_date,
            )
        )
        .table()
    )
    # If Source already present, skip further processing
    if len(t) > 0:
        continue
    # TODO: handle updates?

    # Get the next available Source id
    id = fetch_next_source_id(db, survey="")

    # Convert JSON data into dictionaries for insert
    # ----------------------------------------------

    # Handle publication information
    # Not all references are real papers, may need to have some logic/exclude list
    url_map = process_publications(db=db, data=data)
    if VERBOSE:
        print(url_map)

    # Sources dict
    source_data = [
        {
            "id": id,
            "source_type": "exoplanet",
            "survey": survey,
            "primary_name": primary_name,
            "modification_date": modification_date,
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

    # PlanetProperties dict (just orbital_period for now)
    planet_prop_data = [
        {
            "id": id,
            "orbital_period": extract_from_nested_json(data, "orbital_period", "value"),
            "orbital_period_error": extract_from_nested_json(
                data, "orbital_period", "uerror"
            ),
            "orbital_period_ref": url_map.get(
                extract_from_nested_json(data, "orbital_period", "url")
            ),
            "tess_id": data.get("tess_id"),
        }
    ]

    # Actual ingest of data
    if not DRYRUN:
        with db.engine.connect() as conn:
            conn.execute(db.Sources.insert().values(source_data))
            conn.execute(db.Coords.insert().values(coords_data))
            conn.execute(db.Names.insert().values(names_data))
            conn.execute(db.PlanetProperties.insert().values(planet_prop_data))
            conn.commit()

    count += 1

if not DRYRUN:
    print(f"{count} records added.")

# Calculate elapsed time
end_time = datetime.now()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time.total_seconds() / 60.

print(f"Run time: {start_time} - {end_time}. Total minutes: {elapsed_minutes}")

# No matching of Sources to happen yet- see match_sources.py
