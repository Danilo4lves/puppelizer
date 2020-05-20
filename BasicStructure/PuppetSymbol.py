class PuppetSymbol():
    def __init__(self, symbol):
        self.symbol = symbol

    def accept(self, visitor):
        return visitor.visit_symbol(self)

    def __str__(self):
        return str(self.symbol)
