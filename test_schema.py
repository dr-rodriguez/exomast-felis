# Tests to validate schema in felis yaml format
# Uses Astrodbkit to create the database

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

DB_NAME = "exomast.sqlite"
DB_BASE_NAME = "exomast"

REFERENCE_TABLES = [
    "Publications",
    "Surveys",
]


@pytest.fixture(scope="module")
def schema():
    # Load and validate schema file
    data = yaml.safe_load(open("exomast/schema.yaml", "r"))
    schema = Schema.model_validate(data)
    return schema


@pytest.fixture(scope="module")
def db_object(schema):
    # Build test database

    # Remove any existing copy of the test database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # Using test file for sqlite; in-memory does not preseve inserts
    connection_string = "sqlite:///" + DB_NAME
    engine = create_engine(connection_string)

    # Workaround for SQLite since it doesn't support schema
    with engine.begin() as conn:
        conn.execute(sa.text(f"ATTACH '{DB_NAME}' AS {DB_BASE_NAME}"))

    # Create database from Felis schema
    metadata = MetaDataBuilder(schema).build()
    metadata.create_all(engine)

    # Use AstroDB Database object
    db = Database(connection_string, reference_tables=REFERENCE_TABLES)

    # Confirm DB has been created
    assert os.path.exists(DB_NAME)

    return db


def test_inserts(db_object):
    # Attempt insert with ORM

    engine, metadata = db_object.engine, db_object.metadata

    # Creating basic pointers to the tables
    # If using Felis metadata object (instead of AstroDB.Database), need to include the DB name (astrodb)
    Sources = metadata.tables["Sources"]

    # Data to be loaded, as list of dictionaries
    source_data = [
        {
            "id": 1,
            "type": "exoplanet",
            "survey": "nexsci",
        },
    ]

    # Actual ingest of data
    with engine.connect() as conn:
        conn.execute(Sources.insert().values(source_data))
        conn.commit()