# Exomast Felis


## Getting started

Create a python 3.11 or higher environment

Install package dependencies: `pip install -r requirements.txt`

Validate the schema and produce a sqlite file with `pytest`

If you want to generate ER diagrams you may need to do `conda install -c conda-forge eralchemy2` as it has extra dependencies (graphviz)

## Database design

![database erd](schema/schema.png)

### Docker instructions for a useful Postgres database

This Postgres database is a copy of what was used when testing MOC, so pgsphere and MOC support are installed.

```bash
docker build -f Dockerfile . -t moc-postgres
```

## Test container
```bash
docker run --rm -it moc-postgres /bin/bash
```

The below will create a volume for use and run the container with a postgres user, which you can use in later steps. 

## Run container
```bash
docker volume create moc-pgdata
docker run --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -v moc-pgdata:/var/lib/postgresql/data -d moc-postgres
```

You can then connect to this database with something like Azure Data Studio (may need to install plugins) to manage it. 
You will want to do so to manually create the database: `CREATE DATABASE exomast;` which is what subsequent steps will connect to.

Once you have the Docker container with a blank database set up, you can start running the Felis setup to prepare it.

### Python Environment and Database Setup

Felis requires Python 3.11 or later

```bash
conda create -n exomast-felis python=3.11
conda activate exomast-felis
pip install -r requirements.txt
```

## Felis Setup

The build_postres.py file will take care of setting up the schema, including deleting an old one if it exists.

```bash
python scripts/build_postgres.py
```

If you want TAP_SCHEMA populated you will need to also run:

```bash
sh scripts/build_postgres.sh
```

The above script has some validation checks and outputs a SQL file, but the core of it is:

```bash
felis init-tap postgresql+psycopg://postgres:password@localhost:5432/exomast --tap-schema-name=TAP_SCHEMA
felis load-tap --engine-url=postgresql+psycopg://postgres:password@localhost:5432/exomast --tap-schema-name=TAP_SCHEMA schema/schema.yaml
```

In practice, one can also use felis CLI to prepare the full database, but I found it trickier to use and relied instead on 
AstroDBKit's wrapper for handling the database.

Once that's done, you're ready to migrate data from the old JSON content.

## Migrating Data

The new schema is different, so there is a helper script to convert old JSON content and load it into the database. 
Long term, this would be replaced by brand new ingestion scripts.

You may want to edit the script to point to the correct path to the JSON files. It loads one survey at a time.

```bash
python scripts/ingest_bulk.py
```

## Run Matches

The core of this project is the new Matches table which stores relationships between planets. 
This matching is done after ingestion and thus can be split off from the regular ingestion pipeline.
It does take time, but can be edited to only run on systems updated after some date (there is a modification_date in the DB and JSON files).

```bash
python scripts/match_sources.py
```

### Extra DB Ojbects

There are helper scripts in `sql/checks.sql` to verify the DB contents. 
There is also a helper function that grabs information across matches. 
You can install it by running `sql/build_functions.sql` in Azure Data Studio or similar.