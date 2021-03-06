'''

docker.py: functions for working with docker


'''

from bs4 import BeautifulSoup
from oscookie.logman import bot

from oscookie.utils import (
    check_installed,
    run_command
)

from subprocess import (
    Popen,
    PIPE,
    STDOUT    
)

import requests
import sys

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


def docker_search(term,stars=None,limit=None):
    '''docker_search will use subprocess to do docker search for a dataFrame of
    images
    '''
    if len(check_installed(software='docker')['message']) == 0:
        print("Cannot find Docker, is it installed?")
        sys.exit(1)

    if limit == None:
        limit = 100

    cmd = ['docker','search',term,'--limit',str(limit)]
    if stars != None:
        cmd = cmd + ['--stars',stars]

    result = run_command(cmd)
    if result['return_code'] == 0:
        containers = [x.split(' ')[0] for x in result['message'].decode('utf-8').split('\n')]    
        containers = [x for x in containers if len(x)>0]
        return containers

    bot.logger.warning("Potential problem with search:")
    bot.logger.warning(result['message'])
    return None



def get_dockerfile(image):
    '''get_dockerfile will generate the Dockerfule for an image
    via retrival from the web UI, if available.
    :param image: the full image name to parse
    '''
    parsed = parse_image_uri(image)
    namespace = parsed["namespace"]
    repo_name = parsed["repo_name"]

    url = "https://hub.docker.com/r/%s/%s/~/dockerfile/" %(namespace,repo_name)
    response = requests.get(url).text

    # Rough parsing, but works for now
    soup = BeautifulSoup(response, 'html.parser')

    # Find the dockerfile
    dockerfile = None
    for contender in soup.find_all('div'):
        if contender is not None:
            if contender.get('class') is not None:
                if 'hljs' in contender.get('class'):
                    dockerfile = contender

    # Recreate the lines
    if dockerfile == None:
        return dockerfile

    bot.logger.debug('Found Dockerfile for %s',image)
    return dockerfile.text
            

def parse_image_uri(image,default_namespace=None):
    '''parse_image_uri will return a json structure with a repo name, tag, and
    namespace.
    :param image: the string provided on command line for the image name, eg: ubuntu:latest
    :default_namespace: if not provided, will use "library"
    :returns parsed: a json structure with repo_name, repo_tag, and namespace
    '''
    if default_namespace == None:
        default_namespace = "library"

    image = image.split('/')

    # If there are two parts, we have namespace with repo (and maybe tab)
    if len(image) >= 2:
        namespace = image[0]
        image = image[1]

    # Otherwise, we must be using library namespace
    else:
        namespace = default_namespace
        image = image[0]

    # Now split the docker image name by :
    image = image.split(':')
    if len(image) == 2:
        repo_name = image[0]
        repo_tag = image[1]

    # Otherwise, assume latest of an image
    else:
        repo_name = image[0]
        repo_tag = "latest"

    parsed = {'repo_name':repo_name,
              'repo_tag':repo_tag,
              'namespace':namespace }

    return parsed

