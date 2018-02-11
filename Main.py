for i in range(n_endpoints):
    # read data for each endpoint
    pass


class Endpoint(object):
    def __init__(self, datacentre_latency):
        self.datacentre_latency = datacentre_latency
        self.requests = []


class Cache(object):
    def __init__(self, id, videos):
        self.id = id
        self.videos = videos
        self.endpoints = []


class Request(object):
    def __init__(self, quantity, video):
        self.quantity = quantity
        self.video = video


class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size


def strip_videos(videos, cache_size):
    """ Remove videos that are unrequested
    remove videos that are too large for any of the data centres"""
    returned_videos = videos.copy()

    cnt = 0
    for video in videos:
        if video.size > cache_size:
            returned_videos[cnt].remove()
        cnt += 1



def main():
    connection_latencies = [[]]  # where connection[cache_id][endpoint_id] is the latency between cache and endpoint

    # read data from file
    f = open('me_at_the_zoo.in')
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]

    videos = []
    endpoints = []
    caches = []
    requests = []

    f.close()


if __name__ == '__main__':
    main()
