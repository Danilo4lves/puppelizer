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
