

class ConvertToDictMixin:
    def __init__(self):
        self.fields = []

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item,     '')

    def hide(self, *items):
        for item in items:
            if item not in self.keys():
                continue
            self.fields.remove(item)
        return self

    def append(self, **kwargs):
        for key, value in kwargs.items():
            self.fields.append(key)
            setattr(self, key, value)
        return self
