# Helper script to clear all database tables (not DROP)

import sqlalchemy as sa
import yaml
from config import REFERENCE_TABLES, CONNECTION_STRING, SCHEMA_PATH, SCHEMA_NAME
from astrodbkit.astrodb import Database

db = Database(CONNECTION_STRING, reference_tables=REFERENCE_TABLES, schema=SCHEMA_NAME)

# Get table names
data = yaml.safe_load(open(SCHEMA_PATH, "r"))
table_data = data.get("tables")
table_names = [x.get("name") for x in table_data]
print(table_names)

for name in table_names:
    if name in ["Sources", "Publications"]:
        # Truncate Sources and Publications last
        continue
    db.session.execute(sa.text(f'TRUNCATE "{name}" CASCADE;'))
    db.session.commit()

# Final tables
db.session.execute(sa.text('Truncate "Sources" CASCADE;'))
db.session.commit()
db.session.execute(sa.text('Truncate "Publications" CASCADE;'))
db.session.commit()

print("All tables cleared")
