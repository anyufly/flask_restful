class Module:

    def __init__(self, name, url_prefix=None):
        self.name = name
        self.url_prefix = '/' + url_prefix if url_prefix else '/' + self.name
        self.config = []

    def route(self, rule, **options):
        def decorator(f):
            self.config.append((rule, options, f))
            return f
        return decorator

    def register_to_bp(self, blueprint):
        for rule, options, f in self.config:
            endpoint = options.pop('endpoint', f.__name__)
            blueprint.add_url_rule(self.url_prefix + rule, endpoint, f, **options)
