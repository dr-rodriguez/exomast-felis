# Python script to build the database from the shema.yaml file

import yaml
from astrodbkit.astrodb import Database, create_database

# import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema

CONNECTION_STRING = "postgresql+psycopg://postgres:password@localhost:5432/exomast"
SCHEMA_PATH = "schema/schema.yaml"
DELETE_SCHEMA = True

# Get schema name
data = yaml.safe_load(open(SCHEMA_PATH, "r"))
SCHEMA_NAME = data["name"]
print(f"Preparing for database schema {SCHEMA_NAME}")

# Clear database/schema if requested. Postgres is case-sensitive!
if DELETE_SCHEMA:
    print("Deleting existing schema and database tables")
    engine = create_engine(CONNECTION_STRING)
    with engine.connect() as conn:
        conn.execute(DropSchema(SCHEMA_NAME, cascade=True, if_exists=True))
        conn.execute(DropSchema("TAP_SCHEMA", cascade=True, if_exists=True))
        # conn.execute(sa.text(f"DROP SCHEMA '{SCHEMA_NAME}' CASCADE;"))
        conn.commit()

# AstrodbKit version of creating and connecting to the database
print(f"Creating {SCHEMA_NAME}")
create_database(connection_string=CONNECTION_STRING, felis_schema=SCHEMA_PATH)

# Create TAP_SCHEMA for later use
print("Creating TAP_SCHEMA")
db = Database(connection_string=CONNECTION_STRING, schema=SCHEMA_NAME)
with db.engine.connect() as conn:
    conn.execute(CreateSchema("TAP_SCHEMA", if_not_exists=True))
    conn.commit()

print("Database ready")

# More manual approach:
# from felis.datamodel import Schema
# from felis.metadata import MetaDataBuilder
# from felis.db.utils import DatabaseContext

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
