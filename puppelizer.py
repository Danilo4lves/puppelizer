import json
import pprint
import os
import glob
import subprocess
from BasicStructure import Initiate, Database, Constants
from CodeSmell import UnneccessaryAbstraction, ImperativeAbstraction
from Puppeteer.SmellDetector import AbsSmellDectector
from Puppeteer.SourceModel import SM_File

resultsFile = open(Constants.PUPPET_REPOSITORIES_PATH +
                   '/' + Constants.RESULTS_FILE, 'wt')
resultsFile.write(Constants.RESULTS_FILE_HEADER)


def runPuppeteerOnFile(file):
    fileObj = SM_File.SM_File(file.path)

    count = 0

    for _ in AbsSmellDectector.detectUnnAbsInClasses(fileObj, ""):
        count += 1
    for _ in AbsSmellDectector.detectUnnAbsInModules(fileObj, ""):
        count += 1
    for _ in AbsSmellDectector.detectUnnAbsInDefine(fileObj, ""):
        count += 1

    file.unnecessaryAbsCountPuppeteer = count

    has = False

    for _ in AbsSmellDectector.detectImpAbs(fileObj, ""):
        has = True

    file.hasImperativeAbsPuppeteer = has


def runPuppelizerOnFile(file, isJsonFormatted=False):
    if (not isJsonFormatted):
        PUPPET_PARSER_COMMAND = '/opt/puppetlabs/bin/puppet parser dump --format json ' + \
            file.path + ' > ' + file.path[:-3] + '.json'
        subprocess.run(
            PUPPET_PARSER_COMMAND, shell=True, stdout=subprocess.PIPE)

        with open(file.path[:-3] + '.json') as jsonFile:
            puppetFileInJson = json.load(jsonFile)

        removeJsonFileCommand = 'rm ' + file.path[:-3] + '.json'
        subprocess.run(removeJsonFileCommand, shell=True)
    else:
        with open(file) as jsonFile:
            puppetFileInJson = json.load(jsonFile)

    obj = Initiate.pn_to_python(puppetFileInJson)
    ast = Initiate.construct(obj)

    imperativeAbstractionResults = ImperativeAbstraction.runner(ast)
    unnecessaryAbstractionResult = UnneccessaryAbstraction.runner(ast)

    file.classCount = imperativeAbstractionResults._class
    file.defineCount = imperativeAbstractionResults._define
    file.fileResourceCount = imperativeAbstractionResults._file
    file.packageResourceCount = imperativeAbstractionResults._package
    file.serviceResourceCount = imperativeAbstractionResults._service
    file.execCount = imperativeAbstractionResults._exec
    file.hasImperativeAbs = imperativeAbstractionResults.isSmellPresent
    file.unnecessaryAbsCount = unnecessaryAbstractionResult


def runPuppelizerOnAllFiles():
    filesTested = 0

    files = Database.runner()

    totalFiles = len(files)

    for file in files:
        print('Files tested: ' + str(filesTested) +
              '/' + str(totalFiles))
        print('Current file: ', file.path)

        try:
            if ((file.hasImperativeAbs is None) or (file.unnecessaryAbsCount is None)):
                runPuppelizerOnFile(file)

            if ((file.hasImperativeAbsPuppeteer is None) or (file.unnecessaryAbsCountPuppeteer is None)):
                runPuppeteerOnFile(file)
        except:
            file.hasSyntaxError = True

        file.isAnalyzed = True
        file.save()

        filesTested += 1


runPuppelizerOnAllFiles()
# runPuppelizerOnFile(PUPPET_FILE_PATH)
