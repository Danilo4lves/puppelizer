class PuppetVar:
    def __init__(self, var):
        self.var = var

    def accept(self, visitor):
        return visitor.visit_var(self)

    def __str__(self):
        return "$" + str(self.var)
