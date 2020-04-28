# region ############################# IMPORTS #############################

import logging
from debug import setup_logging
log = logging.getLogger("default")
setup_logging()

import os
from datetime import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase#, FTS5Model, SearchField
from configuration import read_config, write_config
from paths import DATA_DIR

# endregion


# region ############################# GLOBALS #############################
realpath = os.path.dirname(os.path.realpath(__file__))
rp = realpath

db_path = os.path.join(DATA_DIR, 'database.db')
pragmas = [
    ('journal_mode', 'wal'),
    ('cache_size', -1000 * 32)]
db = SqliteExtDatabase(db_path, pragmas=pragmas)

# endregion



# region ############################# TABLE CLASSES #############################

class BroModel(Model):
    date_created = DateTimeField(default=datetime.now())
    date_updated = DateTimeField(default=datetime.now())
    date_deleted = DateTimeField(null=True)
    deleted = BooleanField(default=False)

    def mark_deleted(self):
        self.deleted = True
        self.date_deleted = datetime.now()
        self.save()

class Entry(BroModel):
    filename = TextField()



    class Meta:
        database = db

    def create(self, **query):
        log.debug("Creating new Entry: " + " ".join([self.title]))
        ret = super(Entry, self).create(**query)
        return ret

    def save(self, *args, **kwargs):
        log.debug("Updating Entry info: " + str("") + " - " + str(self.title))
        self.date_updated = datetime.now()
        ret = super(Entry, self).save(*args, **kwargs)

        return ret



# region Migration
config = read_config()
if config['database_migrate']:
    log.debug("=====================")
    log.debug("Migration stuff...")
    try:
        from playhouse.migrate import *

        migrator = SqliteMigrator(db)

        open_count = IntegerField(default=0)

        migrate(
            migrator.add_column('Entry', 'open_count', open_count)
        )
        log.debug("Migration success")
        log.debug("=====================")

        config['database_migrate'] = False
        write_config(config)
    except:
        log.error("Could not migrate", exc_info=True)
        log.debug("=====================")
# endregion

log.info(" ".join(["Using DB", str(db), "At path:", str(db_path)]))

# On init make sure we create database

db.connect()
db.create_tables([Entry])

# endregion
