# Python script to populate database

import os
import pytest
import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import IntegrityError

from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder

from astrodbkit.astrodb import Database


CONNECTION_STRING = "postgresql+psycopg2://postgres:password@localhost:5432/exomast"
# CONNECTION_STRING = "sqlite:///exomast.sqlite"
REFERENCE_TABLES = [
    "Publications",
    "Surveys",
]

# Check if DB/tables exists
engine = create_engine(CONNECTION_STRING)
with Session(engine) as session:
    result = session.execute(sa.text("select * from Sources")).fetchall()
print(result)

db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES)

# Create object for SQLAlchemy use
Sources = db.metadata.tables["Sources"]

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
with engine.connect() as conn:
    conn.execute(Sources.insert().values(source_data))
    conn.commit()

