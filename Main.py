import random

endpoints = []
caches = []
videos = []
requests = []
connection_latencies = [[]]  # where connection[cache_id][endpoint_id] is the latency between cache and endpoint
for i in range(n_endpoints):
    # read data for each endpoint
    pass


class Endpoint(object):
    def __init__(self, id, datacentre_latency):
        self.id = id
        self.datacentre_latency = datacentre_latency
        self.requests = []
        self.caches = []


class Cache(object):
    def __init__(self, id):
        self.id = id
        self.videos = []
        self.endpoints = []


class Request(object):
    def __init__(self, quantity, video):
        self.quantity = quantity
        self.video = video


class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size


def strip_videos(videos, cache_size, requests):
    """ Remove videos that are unrequested
    remove videos that are too large for any of the data centres"""
    requested_IDs = []
    for i in requests:
        requested_IDs.append(i.video.id)

    cnt = 0
    for video in videos:
        if video.size > cache_size or video.id not in requested_IDs:
            videos[cnt].remove()
        cnt += 1
    return videos


def write_to_file(caches):
    """
    Takes in the info about the caches and writes it to output.txt as google wants it formatted

    :param caches: a list of all the caches that we are using.
    :return: nothing, just writes to 'output.txt' the data as google wants it
    """
    text = str(len(caches))
    for cache in caches:
        text += "\n" + str(cache.id) + " "
        for video in cache.videos:
            text += str(video.id) + " "
    output = open("output.txt", "w")
    output.write(text)
    output.close()


def create_dummy_caches():
    """
    Creates dummy caches & dummy videos for those caches within the limits specified by google
    :return: a list of dummy caches, fully populated with videos and cache_id's
    """
    caches = []
    for cache_id in range(random.randint(1, 1000)):
        videos = []
        for video_id in range(random.randint(1, 5)):
            video = Video(random.randint(1, 1000))
            videos.append(video)

        cache = Cache(cache_id, videos)
        caches.append(cache)
    return caches


def get_score():
    """
    Calculates our score from the variables, *NOT* from output.txt
    :return: int: our score as described by google
    """
    for e in endpoints:
        for r in requests:
            for c in caches:
                if e in c.endpoints and r.video in c.videos:
                    pass


def main():
    # read data from file
    f = open('me_at_the_zoo.in')
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]

    for i in range(n_videos):
        videos.append(Video(i, video_sizes[i]))

    for i in range(n_caches):
        caches.append(Cache(i))

    for i in range(n_caches):
        connection_latencies.append([])
        for j in range(n_endpoints):
            connection_latencies[i].append([])

    for i in range(n_endpoints):
        # read data for each endpoint
        datacentre_latency, endpoint_n_caches = [int(part) for part in f.readline().split()]

        endpoints.append(Endpoint(i, datacentre_latency))

        for j in range(endpoint_n_caches):
            cache, latency = [int(part) for part in f.readline().split()]
            endpoints[i].caches.append(caches[cache])
            caches[cache].endpoints.append(endpoints[i])
            connection_latencies[cache][i] = latency

    for i in range(n_videos):
        # read data for each video
        video_id, endpoint_id, n_requests = [int(part) for part in f.readline().split()]

        requests.append(Request(n_requests, videos[video_id]))
        endpoints[endpoint_id].requests.append(requests[i])

    f.close()

    # Strip unneeded videos
    videos = strip_videos()


if __name__ == '__main__':
    main()
