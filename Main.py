endpoints = []
caches = []
videos = []
requests = []
cache_size = 0

connection_latencies = [[]]  # where connection[cache_id][endpoint_id] is the latency between cache and endpoint

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


def read_file(filename):
    f = open(filename)
    n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
    video_sizes = [int(part) for part in f.readline().split()]
    
    for i in range(n_videos):
        videos.append(Video(video_sizes[i]))
    
    for i in range(n_caches):
        caches.append(Cache())
    
    for i in range(n_caches):
        connection_latencies.append([])
        for j in range(n_endpoints):
            connection_latencies[i].append([])
    
    for i in range(n_endpoints):
        # read data for each endpoint
        datacentre_latency, endpoint_n_caches = [int(part) for part in f.readline().split()]
        
        endpoints.append(Endpoint(datacentre_latency))
        
        for j in range(endpoint_n_caches):
            cache, latency = [int(part) for part in f.readline().split()]
            endpoints[i].caches.append(caches[cache])
            caches[cache].endpoints.append(endpoints[i])
            connection_latencies[cache][i] = latency
    
    for i in range(n_request_descriptions):
        # read data for each video
        video_id, endpoint_id, n_requests = [int(part) for part in f.readline().split()]
        
        requests.append(Request(n_requests, videos[video_id]))
        endpoints[endpoint_id].requests.append(requests[i])
    
    f.close()

def strip_videos():
    """ Remove videos that are unrequested
    remove videos that are too large for any of the data centres"""
    
    for video in videos:
        if video.size > cache_size or video not in [request.video for request in requests]:
            videos.remove(video)

    return videos


def main():
    
    read_file('example.in')
    

    #Strip unneeded videos
    videos = strip_videos()


if __name__ == '__main__':
    main()