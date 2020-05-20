import json
import pprint
import os
import glob
import subprocess
from BasicStructure import Initiate
from CodeSmell import UnneccessaryAbstraction, ImperativeAbstraction

PUPPET_FILES_PATH = '/Users/Alves/Desktop/puppetAnalysis'
PUPPET_FILES_PATH_2 = '../puppet-repositories'
PUPPET_FILE_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesInJson/alltypes.json'


def runPuppelizerOnFile(file, isJsonFormatted=False):
    if (not isJsonFormatted):
        puppetParserCommand = '/opt/puppetlabs/bin/puppet parser dump --format json ' + \
            file + ' > ' + file[:-3] + '.json'
        subprocess.run(
            puppetParserCommand, shell=True, stdout=subprocess.PIPE)

        with open(file[:-3] + '.json') as jsonFile:
            puppetFileInJson = json.load(jsonFile)

        removeJsonFileCommand = 'rm ' + file[:-3] + '.json'
        subprocess.run(removeJsonFileCommand, shell=True)
    else:
        with open(file) as jsonFile:
            puppetFileInJson = json.load(jsonFile)

    obj = Initiate.pn_to_python(puppetFileInJson)
    ast = Initiate.construct(obj)

    UnneccessaryAbstraction.runner(ast)
    # ImperativeAbstraction.runner(ast)
    print("\n-------------------\n")


def runPuppelizerOnAllFiles(filesPath):
    for file in os.listdir(filesPath):
        globPathName = filesPath + '/' + file + '/**/*.pp'
        print(globPathName)
        files = glob.glob(globPathName, recursive=True)

        for item in files:
            runPuppelizerOnFile(item)


runPuppelizerOnAllFiles(PUPPET_FILES_PATH_2)
# runPuppelizerOnFile(PUPPET_FILE_PATH, True)
