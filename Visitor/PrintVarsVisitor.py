from Visitor import PuppetVisitor


class PrintVarsVisitor(PuppetVisitor.PuppetVisitor):
    def visit_var(self, obj):
        print("Variable: " + str(obj.var))
        return True
