from Visitor import PuppetVisitor


class DuplicateKeyVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self):
        self.duplicate_keys = set()
        self.keys = set()

    def begin_call(self, call):
        if str(call.func_name) == "=>":
            key = str(call.params[0])

            if key in self.keys:
                self.duplicate_keys.add(key)

            self.keys.add(key)

            return False

        return True
