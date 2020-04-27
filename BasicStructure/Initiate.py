import itertools
from BasicStructure import PuppetMap, PuppetSymbol, PuppetVar, PuppetCall, PuppetList, PuppetString

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
