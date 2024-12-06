#!/bin/bash

# Empty database must be created first with CREATE DATABASE and a schema exomast must also be created with CREATE SCHEMA

felis validate exomast/schema.yaml

felis create --initialize --engine-url postgresql+psycopg2://postgres:password@localhost:5432/exomast exomast/schema.yaml
