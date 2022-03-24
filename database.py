# region ############################# IMPORTS #############################

from debug import get_logger
log = get_logger("default")

import os
from datetime import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase  # , FTS5Model, SearchField
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
    date_created = DateTimeField()
    date_updated = DateTimeField()
    date_deleted = DateTimeField(null=True)
    deleted = BooleanField(default=False)

    class Meta:
        database = db

    def mark_deleted(self):
        self.deleted = True
        self.date_deleted = datetime.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = datetime.now()
            
        self.date_updated = datetime.now()

        super(BroModel, self).save(*args, **kwargs)


class Entry(BroModel):
    filename = TextField()


log.info(" ".join(["Using DB", str(db), "At path:", str(db_path)]))

# On init make sure we create database

db.connect()
db.create_tables([Entry])

# endregion
