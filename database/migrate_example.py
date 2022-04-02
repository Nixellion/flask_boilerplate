"""
Example migration script
"""

# This part is required to be able to run this script directly
#  from within a folder and still import things from the project folder
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Import logger to log things that happen here
from debug import get_logger
log = get_logger("database")

# Import paths module to get a path to database and data dirs
from paths import DATABASE_PATH


try:
    from playhouse.sqlite_ext import CSqliteExtDatabase as SqliteExtDatabase  # , FTS5Model, SearchField
    PEEWEE_CYTHON = True
except:
    from playhouse.sqlite_ext import SqliteExtDatabase
    PEEWEE_CYTHON = False

pragmas = [
    ('journal_mode', 'wal'),
    ('cache_size', -1000 * 32)]

db = SqliteExtDatabase(DATABASE_PATH, pragmas=pragmas)


# Uncomment and adjust as needed
# log.debug("=====================")
# log.debug("Migration in progress...")
# try:
#     from playhouse.migrate import *

#     migrator = SqliteMigrator(db)

#     data_json = TextField(null=True)

#     migrate(
#         migrator.add_column('Event', 'data_json', data_json)
#     )
#     log.debug("Migration success")
#     log.debug("=====================")
# except:
#     log.error("Could not migrate", exc_info=True)
#     log.debug("=====================")
