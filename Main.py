endpoints = []
caches = []
videos = []
requests = []
cache_size = 0

connection_latencies = [[]]  # where connection[cache_id][endpoint_id] is the latency between cache and endpoint

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
        
    def space_remaining(self):
        space_used = 0
        for video in self.videos:
            space_used += video.size
        return cache_size - space_used


class Request(object):
    def __init__(self, id, quantity, video):
        self.id = id
        self.quantity = quantity
        self.video = video


class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size


def strip_videos():
    """ Remove videos that are unrequested
    remove videos that are too large for any of the data centres"""
    requested_IDs = []
    for i in requests:
        requested_IDs.append(i.video.id)

    cnt = 0
    for video in videos:
        if video.size > cache_size or video.id not in requested_IDs:
            del videos[cnt]
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
            video = Video(video_id, random.randint(1, 1000))
            videos.append(video)

        cache = Cache(cache_id)
        caches.append(cache)
    return caches


def get_score():
    """
    Calculates our score from the variables, *NOT* from output.txt
    :return: int: average time (microseconds) saved as described by google (total_time_saved//total_requests)
    Loop through every request coming from every endpoint.
        Check every cache to see if it can satisfy that request.
        Of those caches which can satisfy the request, choose the one with the least latency
        Calculate the time saved, convert to microseconds and add it to total_time_saved
    Calculate the average time saved

    """
    total_time_saved = 0
    
    for endpoint in endpoints:
        for request in endpoint.requests:
            # see if this request is in the cache
            video_in_cache = False
            for cache in endpoint.caches:
                for video in cache.videos:
                    if request.video.id == video.id:
                        video_in_cache = True
                        
            if video_in_cache:
                total_time_saved += request.quantity * (endpoint.datacentre_latency - connection_latencies[cache.id][endpoint.id])
    
    total_requests = 0
    for request in requests:
        total_requests += request.quantity
    
    return (total_time_saved * 1000) / total_requests
    


def read_file(filename):
    global cache_size
    f = open(filename)
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]

    for i in range(n_videos):
        videos.append(Video(i, video_sizes[i]))

    for i in range(n_caches):
        caches.append(Cache(i))

    for i in range(n_caches):
        connection_latencies.append([])
        for j in range(n_endpoints):
            connection_latencies[i].append(0)

    for i in range(n_endpoints):
        # read data for each endpoint
        datacentre_latency, endpoint_n_caches = [int(part) for part in f.readline().split()]

        endpoints.append(Endpoint(i, datacentre_latency))

        for j in range(endpoint_n_caches):
            cache, latency = [int(part) for part in f.readline().split()]
            endpoints[i].caches.append(caches[cache])
            caches[cache].endpoints.append(endpoints[i])
            connection_latencies[cache][i] = latency

    for i in range(n_request_descriptions):
        # read data for each video
        video_id, endpoint_id, n_requests = [int(part) for part in f.readline().split()]

        requests.append(Request(i, n_requests, videos[video_id]))
        endpoints[endpoint_id].requests.append(requests[i])

    f.close()

def main():
    read_file('example.in')

    # Strip unneeded videos
    #videos = strip_videos()
    
    global caches
    
    caches[0].videos.append(videos[0])
    
    caches[1].videos.append(videos[3])
    caches[1].videos.append(videos[1])
    
    caches[2].videos.append(videos[0])
    caches[2].videos.append(videos[1])
    
    print(get_score())
    

    # for endptindx, endpoint in enumerate(endpoints):
    #     while endpoint.requests:
    #         max_request = 0
    #         for request in endpoint.requests:
    #             if request.quantity > max_request:
    #                 max_request = request

    #         min_cacheid = 999999999
    #         for cache in endpoint.caches:
    #             if min_cacheid < connection_latencies[cache.id][endptindx]:
    #                 min_cacheid = connection_latencies[cache.id][endptindx]

    # for e in endpoints:
    #     max_request = e.requests[0]
    #     for r in e.requests:
    #         if r.quantity > max_request.quantity:
    #             max_request = r
    #
    #     min_cache_latency = e.caches[0]
    #     for c in e.caches:
    #         if connection_latencies[c.id][e.id] < connection_latencies[min_cache_latency.id][e.id]:
    #             min_cache_latency = c


            #
            # for r in e.requests:
            #     cache_latency = 999999999
            #     for c in caches:
            #         if e in c.endpoints and r.video in c.videos:
            #             cache_latency = min(connection_latencies[c.id][e.id], cache_latency)

        # total_time_saved += r.quantity * (e.datacentre_latency - min_cache_latency) * 1000
        # total_requests += r.quantity


if __name__ == '__main__':
    main()
