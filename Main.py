# read data from file
f = open('me_at_the_zoo.in')
n_videos, n_endpoints, n_request_descriptions, n_caches, cache_size = [int(part) for part in f.readline().split()]
video_sizes = [int(part) for part in f.readline().split()]

for i in range(n_endpoints):
	# read data for each endpoint
	pass

