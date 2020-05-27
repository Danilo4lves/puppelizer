# https://github.com/coleifer/peewee

import datetime
import glob
import os
from peewee import SqliteDatabase, CharField, BooleanField, IntegerField, Model
from BasicStructure import Constants

db = SqliteDatabase('analysis.db')


class BaseModel(Model):
    class Meta:
        database = db


class PuppetFiles(BaseModel):
    path = CharField(unique=True)
    isAnalyzed = BooleanField(default=False)
    hasSyntaxError = BooleanField(default=False)
    repositoryName = CharField(null=True)
    classCount = IntegerField(null=True)
    defineCount = IntegerField(null=True)
    fileResourceCount = IntegerField(null=True)
    packageResourceCount = IntegerField(null=True)
    serviceResourceCount = IntegerField(null=True)
    execCount = IntegerField(null=True)
    unnecessaryAbsCount = IntegerField(null=True)
    hasImperativeAbs = BooleanField(null=True)


db.connect()
db.create_tables([PuppetFiles])


def runner():
    row_count = (PuppetFiles.select().count())

    if row_count == 0:
        repositories = os.listdir(Constants.PUPPET_REPOSITORIES_PATH)

        for repository in repositories:
            for path in glob.glob(Constants.PUPPET_REPOSITORIES_PATH + "/" + repository + "/**/*.pp", recursive=True):
                print(path, repository)
                PuppetFiles.create(path=path, repositoryName=repository)

    files = (PuppetFiles
             .select()
             .where((PuppetFiles.isAnalyzed == False)))

    return files
