# https://github.com/coleifer/peewee

import datetime
import glob
import os
import sys
from peewee import SqliteDatabase, CharField, BooleanField, IntegerField, Model, fn
from BasicStructure import Constants

db = SqliteDatabase('analysis.db')


class BaseModel(Model):
    class Meta:
        database = db


class PuppetFiles(BaseModel):
    # Common
    path = CharField(unique=True)
    isAnalyzed = BooleanField(default=False)
    hasSyntaxError = BooleanField(default=False)
    repositoryName = CharField(null=True)

    # Puppelizer
    classCount = IntegerField(null=True)
    defineCount = IntegerField(null=True)
    fileResourceCount = IntegerField(null=True)
    packageResourceCount = IntegerField(null=True)
    serviceResourceCount = IntegerField(null=True)
    execCount = IntegerField(null=True)
    unnecessaryAbsCount = IntegerField(null=True)
    hasImperativeAbs = BooleanField(null=True)

    # Puppeteer
    classCountPuppeteer = IntegerField(null=True)
    defineCountPuppeteer = IntegerField(null=True)
    fileResourceCountPuppeteer = IntegerField(null=True)
    packageResourceCountPuppeteer = IntegerField(null=True)
    serviceResourceCountPuppeteer = IntegerField(null=True)
    execCountPuppeteer = IntegerField(null=True)
    unnecessaryAbsCountPuppeteer = IntegerField(null=True)
    hasImperativeAbsPuppeteer = BooleanField(null=True)


db.connect()
db.create_tables([PuppetFiles])


def runner():
    last_repo = PuppetFiles.select(fn.Max(PuppetFiles.repositoryName)).scalar()
    repositories = os.listdir(Constants.PUPPET_REPOSITORIES_PATH)
    for repository in repositories:
        if last_repo is not None and repository <= last_repo:
            print("Ignoring " + repository)
        else:
            print("Adding " + repository)
            entries = []
            for path in glob.glob(Constants.PUPPET_REPOSITORIES_PATH + "/" + repository + "/**/*.pp", recursive=True):
                entries.append((path, repository,))
                print(path, repository)

            with db.atomic():
                PuppetFiles.insert_many(
                    entries, fields=[PuppetFiles.path, PuppetFiles.repositoryName]).execute()

    files = (PuppetFiles
             .select()
             .where((PuppetFiles.isAnalyzed == False)))

    return files
