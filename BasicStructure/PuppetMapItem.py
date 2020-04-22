class PuppetMapItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def accept(self, visitor):
        if visitor.begin_map_item(self):
            self.value.accept(visitor)
        return visitor.end_map_item(self)

    def __str__(self):
        return str(self.key) + ": " + str(self.value)
