# Python script to populate database

import sqlalchemy as sa
from astrodbkit.astrodb import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

CONNECTION_STRING = "postgresql+psycopg://postgres:password@localhost:5432/exomast"
# CONNECTION_STRING = "sqlite:///exomast.sqlite"
REFERENCE_TABLES = [
    "Publications",
    "Surveys",
]

# Check if DB/tables exists
engine = create_engine(CONNECTION_STRING, connect_args={"options": "-csearch_path=exomast"})
with Session(engine) as session:
    # session.execute(sa.text("SET search_path TO exomast"))  # set search path to use the schema
    result = session.execute(sa.text('select * from "Sources"')).fetchall()  # need quotes for case sensitivity
print(result)

db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema="exomast")

# Data to be loaded, as list of dictionaries
source_data = [
    {
        "id": 1,
        "type": "exoplanet",
        "survey": "nexsci",
        "name": "HAT-P-11 b",
    },
]

# Actual ingest of data
with db.engine.connect() as conn:
    conn.execute(db.Sources.insert().values(source_data))
    conn.commit()

# ORM example
# Fails due to backref issue; maybe something related to the foreign keys:
# sqlalchemy.exc.ArgumentError: Error creating backref 'sources_collection' on relationship 'Sources.sources_collection': property of that name exists on mapper 'Mapper[Sources(Sources)]'
# Base = automap_base(metadata=db.metadata)
# Base.prepare()

# # Creating the actual Table objects
# Sources = Base.classes.Sources

# # Adding and removing a basic source
# s = Sources(id=2, name="V4046 Sgr", survey="None", type="star")
# with db.session as session:
#     session.add(s)
#     session.commit()

t = db.query(db.Sources).table()
print(t)
