from BasicStructure import PuppetMapItem


class PuppetMap:
    def __init__(self, map):
        self.items = [PuppetMapItem.PuppetMapItem(
            k, v) for k, v in map.items()]

    def get(self, key):
        value = None
        for item in self.items:
            if key == str(item.key):
                return item.value
        return value

    def accept(self, visitor):
        if visitor.begin_map(self):
            for x in self.items:
                if not x.accept(visitor):
                    break
        return visitor.end_map(self)

    def __str__(self):
        list_str = [str(x) for x in self.items]
        return "\n".join(list_str)
