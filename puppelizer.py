import json
import itertools
import pprint

puppetJsonFile = 'puppet-files/puppet-2.json'

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

class PuppetMap:
    def __init__(self, map):
        self.items = [PuppetMapItem(k, v) for k, v in map.items()]

    def get(self, key):
        value = None
        for item in self.items:
            if key == str(item.key):
                return item.value
        return value

    def accept(self, visitor):
        if visitor.begin_map(self):
            for x in self.items:
                if not x.accept(visitor):
                    break
        return visitor.end_map(self)

    def __str__(self):
        list_str = [str(x) for x in self.items]
        return "\n".join(list_str)

class PuppetMapItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def accept(self, visitor):
        if visitor.begin_map_item(self):
            self.value.accept(visitor)
        return visitor.end_map_item(self)

    def __str__(self):
        return str(self.key) + ": " + str(self.value)

class PuppetCall:
    def __init__(self, func_name, params):
        self.func_name = func_name
        self.params = params

    def accept(self, visitor):
        if visitor.begin_call(self):
            for x in self.params:
                if not x.accept(visitor):
                    break
        return visitor.end_call(self)

    def __str__(self):
        # print(self.func_name)
        if self.params == [None]:
            return self.func_name + "()"
        else:
            params_str = [str(p) for p in self.params]
            return self.func_name + "(" + ", ".join(params_str) + ")"

class PuppetList:
    def __init__(self, list):
        self.list = list

    def accept(self, visitor):
        if visitor.begin_list(self):
            for x in self.list:
                if not x.accept(visitor):
                    break
        return visitor.end_list(self)

    def __str__(self):
        list_str = [str(x) for x in self.list]
        return "\n".join(list_str)

class PuppetString:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_string(self)

    def __str__(self):
        return str(self.value)

class PuppetVar:
    def __init__(self, var):
        self.var = var

    def accept(self, visitor):
        return visitor.visit_var(self)

    def __str__(self):
        return "$" + str(self.var)

class PuppetSymbol():
    def __init__(self, symbol):
        self.symbol = symbol

    def accept(self, visitor):
        return visitor.visit_symbol(self)

    def __str__(self):
        return str(self.symbol)

class PuppetClass():
    def __init__(self, bodies):
        self.bodies = bodies

    def accept(self, visitor):
        return visitor.visit_class(self)
    
    def __str__(self):
        return str(self.bodies)

def construct(obj):
    if type(obj) == dict:
        res = {k: construct(v) for k, v in obj.items()}
        resPuppetMap = PuppetMap(res)
        # resPuppetMapTypeStr = str(resPuppetMap.get('type'))

        # if (resPuppetMapTypeStr == 'class'):
        #     bodies = res['bodies']

        #     return PuppetClass(bodies)

        return resPuppetMap
    elif type(obj) == tuple:
        func_name = obj[0]
        params = [construct(x) for x in obj[1:]]

        if func_name == "qn":
            return PuppetSymbol(params[0])
        elif func_name == "var":
            return PuppetVar(params[0])
        else:
            # print(params)
            return PuppetCall(func_name, params)
    elif type(obj) == list:
        res = [construct(x) for x in obj]

        return PuppetList(res)
    else:
        return PuppetString(obj)

# http://hauchee.blogspot.com/2015/07/hierarchical-visitor-pattern-code.html

class PuppetVisitor:
    def visit_var(self, obj):
        return True

    def visit_string(self, obj):
        return True

    def visit_symbol(self, obj):
        return True

    def visit_class(self, obj):
        return True

    def begin_map(self, obj):
        return True

    def end_map(self, obj):
        return True

    def begin_map_item(self, obj):
        return True

    def end_map_item(self, obj):
        return True

    def begin_list(self, obj):
        return True

    def end_list(self, obj):
        return True

    def begin_call(self, obj):
        return True

    def end_call(self, obj):
        return True

class PrintVarsVisitor(PuppetVisitor):
    def visit_var(self, obj):
        print("Variable: " + str(obj.var))
        return True

class DuplicateKeyVisitor(PuppetVisitor):
    def __init__(self):
        self.duplicate_keys = set()
        self.keys = set()

    def begin_call(self, call):
        if str(call.func_name) == "=>":
            key = str(call.params[0])
            # print(key)
            if key in self.keys:
                self.duplicate_keys.add(key)
            self.keys.add(key)
            return False
        return True

class ClassVisitorBase(PuppetVisitor):
    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            return True
        return False
    
    def begin_map(self, obj):
        if (str(obj.get('type')) == 'class'):
            return True
        return False

class EmptyClassBodyVisitor(ClassVisitorBase):
    def begin_list(self, obj):
        objBodies = obj.list[0]
        classBodyStr = str(objBodies.get('ops'))

        if (len(classBodyStr) == 0):
            print('Class with empty body')

            return False

        return True

class EmptyClassTitleVisitor(ClassVisitorBase):
    def begin_list(self, obj):
        objBodies = obj.list[0]
        classTitleStr = str(objBodies.get('title'))

        if (len(classTitleStr) == 0):
            print('Class with empty title')

            return False

        return True


with open(puppetJsonFile) as json_file:
    data = json.load(json_file)

    obj = pn_to_python(data)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(obj)
    print("\n-------------------\n")

    ast = construct(obj)

    visitor = PrintVarsVisitor()
    ast.accept(visitor)

    print("\n-------------------\n")

    visitor = DuplicateKeyVisitor()
    ast.accept(visitor)
    print("Duplicate keys: " + str(visitor.duplicate_keys))

    visitor = EmptyClassBodyVisitor()
    ast.accept(visitor)

    visitor = EmptyClassTitleVisitor()
    ast.accept(visitor)
