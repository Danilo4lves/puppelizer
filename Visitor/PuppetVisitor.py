# http://hauchee.blogspot.com/2015/07/hierarchical-visitor-pattern-code.html


class PuppetVisitor:
    def visit_var(self, obj):
        return True

    def visit_string(self, obj):
        return True

    def visit_symbol(self, obj):
        return True

    def visit_class(self, obj):
        return True

    def begin_map(self, obj):
        return True

    def end_map(self, obj):
        return True

    def begin_map_item(self, obj):
        return True

    def end_map_item(self, obj):
        return True

    def begin_list(self, obj):
        return True

    def end_list(self, obj):
        return True

    def begin_call(self, obj):
        return True

    def end_call(self, obj):
        return True
