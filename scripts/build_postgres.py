# Python script to build the database from the shema.yaml file

import yaml
import sqlalchemy as sa
from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.exc import IntegrityError
from sqlalchemy.schema import CreateSchema

# from felis.datamodel import Schema
# from felis.metadata import MetaDataBuilder
# from felis.db.utils import DatabaseContext
from astrodbkit.astrodb import create_database, Database

CONNECTION_STRING = "postgresql+psycopg://postgres:password@localhost:5432/exomast"
SCHEMA_PATH = "exomast/schema.yaml"
DELETE_SCHEMA = True

# Get schema name
data = yaml.safe_load(open(SCHEMA_PATH, "r"))
SCHEMA_NAME = data["name"]

# Clear database/schema if requested
if DELETE_SCHEMA:
    engine = create_engine(CONNECTION_STRING)
    with engine.connect() as conn:
        conn.execute(sa.text(f"DROP SCHEMA {SCHEMA_NAME} CASCADE;"))
        conn.commit()

# AstrodbKit version of creating and connecting to the database
create_database(connection_string=CONNECTION_STRING, felis_schema=SCHEMA_PATH)

# Create TAP_SCHEMA for later use
db = Database(connection_string=CONNECTION_STRING, schema=SCHEMA_NAME)
with db.engine.connect() as conn:
    conn.execute(CreateSchema("TAP_SCHEMA", if_not_exists=True))
    conn.commit()


# More manual approach:

# Load and validate schema file
# data = yaml.safe_load(open(SCHEMA_PATH, "r"))
# schema = Schema.model_validate(data)

#  # Create database from Felis schema
# metadata = MetaDataBuilder(schema).build()

# # Create the database
# engine = create_engine(CONNECTION_STRING)
# schema_name = "exomast"
# with engine.connect() as connection:
#     connection.execute(CreateSchema(schema_name, if_not_exists=True))
#     connection.commit()
# metadata.create_all(engine)
