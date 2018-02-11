class Endpoint(object):
    def __init__(self, datacentre_latency):
        self.datacentre_latency = datacentre_latency
        self.requests = []
        self.caches = []


class Cache(object):
    def __init__(self):
        self.videos = []
        self.endpoints = []


class Request(object):
    def __init__(self, quantity, video):
        self.quantity = quantity
        self.video = video


class Video(object):
    def __init__(self, size):
        self.size = size


def main():
    endpoints = []
    caches = []
    videos = []
    connection_latencies = [[]] # where connection[cache_id][endpoint_id] is the latency between cache and endpoint
    
    # read data from file
    f = open('me_at_the_zoo.in')
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]
    
    for i in range(n_videos):
        videos.append(Video(video_sizes[i]))
    
    for i in range(n_caches):
        caches.append(Cache())

    for i in range(n_endpoints):
        # read data for each endpoint
        datacentre_latency, endpoint_n_caches = [int(part) for part in f.readline().split()]
        
        endpoints.append(Endpoint(datacentre_latency))
        
        for j in range(endpoint_n_caches):
            cache, latency = [int(part) for part in f.readline().split()]
            endpoints[i].caches.append(caches[cache])
            # connection_latencies[cache][i] = latency TODO: FIX THIS
            
    for i in range(n_videos):
        # read data for each video
        video_id, endpoint_id, n_requests = [int(part) for part in f.readline().split()]
        
    
    f.close()


if __name__ == '__main__':
    main()