# read data from file
f = open('me_at_the_zoo.in')
n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
video_sizes = [int(part) for part in f.readline().split()]

for i in range(n_endpoints):
    # read data for each endpoint
    pass


class Endpoint(object):
    def __init__(self, id, latency, caches, requests):
        self.id = id
        self.latency = latency
        self.caches = caches
        self.requests = requests


class Cache(object):
    def __init__(self, id, videos):
        self.id = id
        self.videos = videos

class Request(object):
    def __init__(self, quantity, video):
        self.quantity = quantity
        self.video = video

class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size