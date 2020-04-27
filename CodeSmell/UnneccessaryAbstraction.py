from BasicStructure import PuppetVisitor


def runner(ast):
    unneccessaryAbstractionCounter = 0

    visitor = ResourceLikeClass()
    ast.accept(visitor)

    unneccessaryAbstractionCounter += visitor.smellCount

    visitor = IncludeLikeClass()
    ast.accept(visitor)

    unneccessaryAbstractionCounter += visitor.smellCount

    visitor = Define()
    ast.accept(visitor)

    unneccessaryAbstractionCounter += visitor.smellCount

    print('Unneccessary Abstraction: ', unneccessaryAbstractionCounter)


class ResourceLikeClassVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0
        self.isCallResourceMyParent = False
        self.isMapClassMyParent = False

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            self.isCallResourceMyParent = True

            return True

        self.isCallResourceMyParent = False

        return False

    def begin_map(self, obj):
        objType = str(obj.get('type'))

        if ((objType == 'class')):
            self.isMapClassMyParent = True

            return True

        self.isMapClassMyParent = False

        return False

    def begin_list(self, obj):
        objBodies = obj.list[0]
        objBodiesOps = str(objBodies.get('ops'))
        objBodiesOpsLenEqualsZero = len(objBodiesOps) == 0

        if (objBodiesOpsLenEqualsZero & self.isMapClassMyParent & self.isCallResourceMyParent):
            self.smellCount += 1

        self.isCallResourceMyParent = False
        self.isMapClassMyParent = False

        return True


class IncludeLikeClassVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0
        self.isCallClassMyParent = False

    def begin_call(self, call):
        if (str(call.func_name) == 'class'):
            self.isCallClassMyParent = True

            return True

        return False

    def begin_map(self, obj):
        objBody = str(obj.get('body'))

        if (self.isCallClassMyParent & (objBody == 'None')):
            self.smellCount += 1

        self.isCallClassMyParent = False

        return True


class DefineVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0
        self.isCallDefineMyParent = False

    def begin_call(self, call):
        if (str(call.func_name) == 'define'):
            self.isCallDefineMyParent = True

            return True

        self.isCallDefineMyParent = False

        return False

    def begin_map(self, obj):
        objBody = str(obj.get('body'))

        if (self.isCallDefineMyParent & (objBody == 'None')):
            self.smellCount += 1

        self.isCallDefineMyParent = False

        return True
