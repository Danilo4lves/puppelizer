class PuppetString:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_string(self)

    def __str__(self):
        return str(self.value)
