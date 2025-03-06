#!/usr/bin/env python

import requests
import os
import sys
import utils

def get_sha():

    token = os.getenv('GH_AUTH_TOKEN') # In a GitHub workflow, set `AUTH_TOKEN=$(echo ${{ secrets.GITHUB_TOKEN }} | base64)`
    if token:
        utils.logger.info('GH_AUTH_TOKEN env variable is available, using it for authentication')
    else:
        utils.logger.info('GH_AUTH_TOKEN is not available, calling authentication API')
        auth_req = requests.get('https://ghcr.io/token?scope=repository:nvidia/gpu-operator:pull', allow_redirects=True,
                                headers={'Content-Type': 'application/json'})
        auth_req.raise_for_status()
        token = auth_req.json()['token']

    req = requests.get('https://ghcr.io/v2/nvidia/gpu-operator/gpu-operator-bundle/manifests/main-latest', headers={
        'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
    req.raise_for_status()
    return req.json()['config']['digest']

if __name__ == '__main__':
    sha = get_sha()
    utils.update_key(sys.argv[1], 'gpu-main-latest', sha, None)