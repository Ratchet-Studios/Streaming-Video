import random
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
    output = open("output.txt","w")
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
            video = Video(video_id, random.randint(1, 1000))
            videos.append(video)

        cache = Cache(cache_id, videos)
        caches.append(cache)
    return caches


def main():
	connection_latencies = [[]] # where connection[cache_id][endpoint_id] is the latency between cache and endpoint

    # read data from file
    f = open('me_at_the_zoo.in')
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]

    f.close()


if __name__ == '__main__':
    main()