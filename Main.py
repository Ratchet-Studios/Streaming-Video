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
    total_requests = 0
    for e in endpoints:
        for r in requests:
            cache_latency = 999999999
            for c in caches:
                if e in c.endpoints and r.video in c.videos:
                    cache_latency = min(connection_latencies[c.id][e.id], cache_latency)
            total_time_saved += r.quantity * (e.datacentre_latency - cache_latency) * 1000
            total_requests += r.quantity
    return total_time_saved // total_requests


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
    videos = strip_videos()
    
    print('hi')

    timesaved_video_cache = []

    for video in range(len(videos)):
        for cache in range(len(caches)):
            # print('cache ' + str(cache) + ' space remaining: ' + str(caches[cache].space_remaining()))
            if videos[video].size <= caches[cache].space_remaining():
                # calculate time saved by adding video to cache
                timesaved = 0
                for endpoint in caches[cache].endpoints:
                    for request in endpoint.requests:
                        if request.video.id == video:
                            timesaved += request.quantity * (endpoint.datacentre_latency - connection_latencies[cache][endpoint.id])
                
                timesaved_video_cache.append((timesaved, video, cache))

    timesaved_video_cache.sort(key=lambda x: x[0], reverse=True) # sort by time saved
    
    for time, video, cache in timesaved_video_cache:
        print('time saved: {}, when video {} is added to cache {}'.format(time, video, cache))

    while timesaved_video_cache:  # while not empty
        # add video to cache (which saves most time)
        time, video, cache = timesaved_video_cache[0]
        caches[cache].videos.append(videos[video]) #action 1
        del timesaved_video_cache[0]
    
        # update the timesaved_video_cache list so it can be reused without recalculating and sorting every time
        space_remaining_on_cache = caches[cache].space_remaining()

        for i in range(len(timesaved_video_cache) - 1, -1, -1): #according to stackoverflow I have to go backwards to avoid problems
            timesaved2, video2, cache2 = timesaved_video_cache[i]
            
            #adding video2 to cache2 would now be impossible due to #action 1
            if video2 == video or (cache2 == cache and videos[video2].size > space_remaining_on_cache):
                del timesaved_video_cache[i]
        
    for index, cache in enumerate(caches):
        print('Cache ' + str(index) + ' contains:')
        for video in cache.videos:
            print('Video ' + str(video.id))


if __name__ == '__main__':
    main()
