#!/bin/bash

# Empty database must be created first with CREATE DATABASE

felis validate --check-description schema/schema.yaml

# Use --initialize or --drop to create a brand new database, otherwise it will update the existing one
# May want to manually drop with: DROP SCHEMA exomast CASCADE;
# felis create --drop --engine-url postgresql+psycopg://postgres:password@localhost:5432/exomast schema/schema.yaml
felis create --engine-url postgresql+psycopg://postgres:password@localhost:5432/exomast schema/schema.yaml --output-file schema/schema.sql

# TAP metadata initialization and load
# Requires the schema to be created first and specified in the call
echo "Loading TAP_SCHEMA..."
felis init-tap postgresql+psycopg://postgres:password@localhost:5432/exomast --tap-schema-name=TAP_SCHEMA
felis load-tap --engine-url=postgresql+psycopg://postgres:password@localhost:5432/exomast --tap-schema-name=TAP_SCHEMA schema/schema.yaml
