#!/bin/bash

# Empty database must be created first with CREATE DATABASE

felis validate --check-description exomast/schema.yaml

# Use --initialize or --drop to create a brand new database, otherwise it will update the existing one
felis create --drop --engine-url postgresql+psycopg://postgres:password@localhost:5432/exomast exomast/schema.yaml
# felis create --engine-url postgresql+psycopg://postgres:password@localhost:5432/exomast exomast/schema.yaml --output-file exomast/schema.sql
