# Generate an ER diagram for the database

import yaml
from eralchemy2 import render_er
from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder

# Load up schema
data = yaml.safe_load(open("schema/schema.yaml", "r"))
schema = Schema.model_validate(data)

# Create from Felis schema
metadata = MetaDataBuilder(schema).build()

# Show ER model from here
filename = "schema/schema.png"
render_er(metadata, filename)

# Can also generate markdown (mode=mermaid or mermaid_er)
render_er(metadata, "schema/schema.md", mode="mermaid_er")