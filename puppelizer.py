import json
import pprint
import os
import glob
import subprocess
from BasicStructure import Initiate
from CodeSmell import UnneccessaryAbstraction

PUPPET_FILES_PATH = '/Users/Alves/Desktop/puppetAnalysis'
PUPPET_FILES_PATH_2 = '../puppetAnalysis'
PUPPET_FILE_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson/define_with-body.json'


def runPuppelizerOnFile(file):
    puppetParserCommand = '/opt/puppetlabs/bin/puppet parser dump --format json ' + file
    subprocessObject = subprocess.run(
        puppetParserCommand, shell=True, stdout=subprocess.PIPE)
    subprocessOutput = str(subprocessObject.stdout)
    puppetFileInJson = json.loads(subprocessOutput[2:-3])

    obj = Initiate.pn_to_python(puppetFileInJson)
    ast = Initiate.construct(obj)

    UnneccessaryAbstraction.runner(ast)
    print("\n-------------------\n")


def runPuppelizerOnAllFiles(filesPath):
    globPathName = filesPath + '/**/*.pp'
    files = glob.glob(globPathName, recursive=True)

    for item in files:
        runPuppelizerOnFile(item)


runPuppelizerOnAllFiles(PUPPET_FILES_PATH_2)
# runPuppelizerOnFile(PUPPET_FILE_PATH)
