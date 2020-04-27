import json
import pprint
import os
from BasicStructure import Initiate
from CodeSmell import UnneccessaryAbstraction

PUPPET_FILES_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson'
# PUPPET_FILE_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson/class_include-like--with-body.json'
# PUPPET_FILE_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson/class_empty-include-like.json'
PUPPET_FILE_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson/2014_puppet-cdh_hive.json'


def runPuppelizerOnFile(file):
    with open(file) as jsonFile:
        data = json.load(jsonFile)

        obj = Initiate.pn_to_python(data)
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(obj)

        ast = Initiate.construct(obj)

        print(jsonFile)

        # visitor = PrintVarsVisitor()
        # ast.accept(visitor)

        # print("\n-------------------\n")

        # visitor = DuplicateKeyVisitor()
        # ast.accept(visitor)
        # print("Duplicate keys: " + str(visitor.duplicate_keys))

        UnneccessaryAbstraction.runner(ast)
        print("\n-------------------\n")

        # visitor = EmptyClassTitleVisitor()
        # ast.accept(visitor)


def runPuppelizerOnAllFiles(filesPath):
    # totalRepos = len(os.listdir(PUPPET_FILES_PATH))

    for item in os.listdir(filesPath):
        currentFile = filesPath + '/' + item

        runPuppelizerOnFile(currentFile)


runPuppelizerOnAllFiles(PUPPET_FILES_PATH)
# runPuppelizerOnFile(PUPPET_FILE_PATH)
