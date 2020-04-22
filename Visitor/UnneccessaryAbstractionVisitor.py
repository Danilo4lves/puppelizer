from Visitor import PuppetVisitor


class UnneccessaryAbstractionVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            return True
        return False

    def begin_map(self, obj):
        objType = str(obj.get('type'))
        objBodies = str(obj.get('bodies'))

        if ((objType == 'class') & (len(objBodies) == 0)):
            self.smellCount += 1

            return True
        return False
