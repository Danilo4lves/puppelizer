from Visitor import PuppetVisitor


class ResourceLikeClass(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            return True
        return False

    def begin_map(self, obj):
        objType = str(obj.get('type'))

        if ((objType == 'class')):
            return True
        return False

    def begin_list(self, obj):
        objBodies = obj.list[0]
        objBodiesOps = str(objBodies.get('ops'))

        if (len(objBodiesOps) == 0):
            self.smellCount += 1

        return False


class IncludeLikeClass(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.smellCount = 0

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            return True
        return False

    def begin_map(self, obj):
        objType = str(obj.get('type'))
        objBody = str(obj.get('body'))

        if ((objType == 'class') & (len(objBody) == 0)):
            self.smellCount += 1

        return False
