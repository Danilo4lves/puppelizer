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
        if self.params == [None]:
            return self.func_name + "()"
        else:
            params_str = [str(p) for p in self.params]
            return self.func_name + "(" + ", ".join(params_str) + ")"
