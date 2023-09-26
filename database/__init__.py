# region ############################# IMPORTS #############################

# region Logger
from loguru import logger as log
# endregion

import os
from datetime import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase  # , FTS5Model, SearchField
from configuration import read_config, write_config
from paths import DATABASE_PATH
import uuid

# endregion


# region ############################# GLOBALS #############################
realpath = os.path.dirname(os.path.realpath(__file__))
rp = realpath

pragmas = [
    ('journal_mode', 'wal'),
    ('cache_size', -1000 * 32)]
db = SqliteExtDatabase(DATABASE_PATH, pragmas=pragmas)


# endregion


# region ############################# TABLE CLASSES #############################

class BroModel(Model):
    # Uncomment to use UUIDs globally. Peewee can take FUNCTIONS\callables as default values.
    # Make sure NOT TO INCLUDE brackets
    # id = UUIDField(primary_key=True, default=uuid.uuid4)
    date_created = DateTimeField(default=datetime.now)
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
        self.date_updated = datetime.now()

        super(BroModel, self).save(*args, **kwargs)


class Entry(BroModel):
    filename = TextField()


log.info(" ".join(["Using DB", str(db), "At path:", str(DATABASE_PATH)]))

# On init make sure we create database

db.connect()
db.create_tables([Entry])

# endregion
