# Exomast Felis


## Getting started

Create a python 3.11 or higher environment

Install package dependencies: `pip install -r requirements.txt`

Validate the schema and produce a sqlite file with `pytest`

If you want to generate ER diagrams you may need to do `conda install -c conda-forge eralchemy2` as it has extra dependencies (graphviz)

## Database design

![database erd](exomast/schema.png)

## Docker instructions for a useful Postgres database
```bash
docker build -f Dockerfile . -t moc-postgres
```

## Test container
```bash
docker run --rm -it moc-postgres /bin/bash
```

## Run container
```bash
docker volume create moc-pgdata
docker run --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -v moc-pgdata:/var/lib/postgresql/data -d moc-postgres
```