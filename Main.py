class Endpoint(object):
    def __init__(self, id, latency, caches):
        self.id = id
        self.latency = latency
        self.caches = caches

class Cache(object):
    def __init__(self, id, videos):
        pass