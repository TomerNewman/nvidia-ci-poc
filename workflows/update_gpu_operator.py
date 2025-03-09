#!/usr/bin/env python

import requests
import re
import utils
import sys

def get_operator_versions():
    logger = utils.get_logger()
    logger.info('Calling NVCR authentication API')
    auth_req = requests.get('https://nvcr.io/proxy_auth?scope=repository:nvidia/gpu-operator:pull', allow_redirects=True,
                                headers={'Content-Type': 'application/json'})
    auth_req.raise_for_status()
    token = auth_req.json()['token']

    logger.info('Listing tags of the operator image')
    req = requests.get('https://nvcr.io/v2/nvidia/gpu-operator/tags/list', headers={
        'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
    req.raise_for_status()

    tags = req.json()['tags']
    prog = re.compile(r'^v(2\d\.\d+)\.\d+$')
    versions = {}
    for t in tags:
        match = prog.match(t)
        if match:
            minor = match.group(1)
            existing = versions.get(minor)
            if not existing or existing < t:
                versions[minor] = t
    return versions

def version2suffix(v):
    return f'{v.replace(".", "-")}-x'

def get_latest_versions_as_suffix(versions):
    return [version2suffix(v) for v in sorted(versions)[-2:]]

if __name__ == "__main__":
    versions = get_operator_versions()
    utils.update_key(sys.argv[1], 'gpu-operator', versions)
