#!/usr/bin/env python

from oscookie.docker import (
    docker_search,
    get_dockerfile,
    parse_image_uri
)

import pickle

dockerfiles = dict()

######################################################################
# Download Dockerfiles
######################################################################

terms = ['science','genetics','neuro','bio','python','data']

# Let's make sure not to take repeat containers from different users
seen = []

for term in terms:
    containers = docker_search(term)
    for container in containers:
        if container not in dockerfiles:
            try:
                parsed = parse_image_uri(container)
                if parsed['repo_name'] not in seen:
                    df = get_dockerfile(container)
                    if df != None:
                        dockerfiles[container] = df
                    seen.append(parsed['repo_name'])
            except:
                print('Skipping %s'%container)

print("Found %s dockerfiles." %(len(dockerfiles))) # 303
pickle.dump(dockerfiles,open('dockerfiles.pkl','wb'))
    
