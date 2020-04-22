import json
import itertools
import pprint
import os
from BasicStructure import PuppetMap, PuppetSymbol, PuppetVar, PuppetCall, PuppetList, PuppetString
from Visitor import UnneccessaryAbstractionVisitor

puppetJsonFile = 'puppet-files/puppet-2.json'
PUPPET_FILES_PATH = '/Users/Alves/Desktop/puppetAnalysis/filesinjson'

# Input: JSON object representing a Puppet file in Puppet Notation (PN)
# Output: object representing the same file using regular Python objects,
#         such as dicts, tuples, and lists.
#         Tuples represent function calls using infix notation


def pn_to_python(node):
    if type(node) == dict:
        if "^" in node:
            # Function call
            res = [pn_to_python(elem) for elem in node["^"]]
            return tuple(res)
        elif "#" in node:
            # Hash/dict
            res = [pn_to_python(elem) for elem in node["#"]]
            # Convert [a, b, c, d] to {a: b, c: d}
            return dict(itertools.zip_longest(*[iter(res)] * 2, fillvalue=""))
    elif type(node) == list:
        return [pn_to_python(elem) for elem in node]
    else:
        return node


def construct(obj):
    if type(obj) == dict:
        res = {k: construct(v) for k, v in obj.items()}
        resPuppetMap = PuppetMap.PuppetMap(res)

        return resPuppetMap
    elif type(obj) == tuple:
        func_name = obj[0]
        params = [construct(x) for x in obj[1:]]

        if func_name == "qn":
            return PuppetSymbol.PuppetSymbol(params[0])
        elif func_name == "var":
            return PuppetVar.PuppetVar(params[0])
        else:
            # print(params)
            return PuppetCall.PuppetCall(func_name, params)
    elif type(obj) == list:
        res = [construct(x) for x in obj]

        return PuppetList.PuppetList(res)
    else:
        return PuppetString.PuppetString(obj)


# with open(puppetJsonFile) as json_file:
# with open(PUPPET_FILES_PATH + '/' + 'puppet-1.pp') as json_file:
#     data = json.load(json_file)
#     print('json', json_file)

#     obj = pn_to_python(data)
#     pp = pprint.PrettyPrinter(indent=2)
#     pp.pprint(obj)
#     print("\n-------------------\n")

#     ast = construct(obj)

#     visitor = PrintVarsVisitor()
#     ast.accept(visitor)

#     print("\n-------------------\n")

#     visitor = DuplicateKeyVisitor()
#     ast.accept(visitor)
#     print("Duplicate keys: " + str(visitor.duplicate_keys))

#     visitor = UnneccessaryAbstractionVisitor()
#     ast.accept(visitor)

#     visitor = EmptyClassTitleVisitor()
#     ast.accept(visitor)


totalRepos = len(os.listdir(PUPPET_FILES_PATH))

count = 0
unneccessaryAbstractionCounter = 0

for item in os.listdir(PUPPET_FILES_PATH):
    currentFile = os.path.join(PUPPET_FILES_PATH, item)
    currentFile = PUPPET_FILES_PATH + '/' + item

    # print(str(count) + "of " + str(totalRepos) + " : " + str(currentFolder) + str(item))

    with open(currentFile) as json_file:
        data = json.load(json_file)

        obj = pn_to_python(data)
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(obj)
        # print("\n-------------------\n")

        ast = construct(obj)

        # visitor = PrintVarsVisitor()
        # ast.accept(visitor)

        # print("\n-------------------\n")

        # visitor = DuplicateKeyVisitor()
        # ast.accept(visitor)
        # print("Duplicate keys: " + str(visitor.duplicate_keys))

        visitor = UnneccessaryAbstractionVisitor.UnneccessaryAbstractionVisitor()
        ast.accept(visitor)
        unneccessaryAbstractionCounter += visitor.smellCount

        # visitor = EmptyClassTitleVisitor()
        # ast.accept(visitor)

print('Unneccessary Abstraction Counter: ', unneccessaryAbstractionCounter)
