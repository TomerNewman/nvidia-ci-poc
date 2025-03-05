#!/usr/bin/env python

from ngcsdk import Client
from registry.api import image
import os
import re
import utils
import sys

if __name__ == "__main__":
    # https://docs.ngc.nvidia.com/sdk/index.html
    c = Client()
    api_key = os.getenv('API_KEY') # https://org.ngc.nvidia.com/setup/api-keys
    c.configure(api_key=api_key, org_name='kse5libxgpiz', team_name='no-team', ace_name='no-ace')
    i = image.ImageAPI(c)

    prog = re.compile(r'^v(2\d\.\d+)\.\d+$')
    versions = {}
    for i in i.list_images('nvidia/gpu-operator'):
        match = prog.match(i.tag)
        if match:
            minor = match.group(1)
            existing = versions.get(minor)
            if not existing or existing < i.tag:
                versions[minor] = i.tag

    utils.update_keys(sys.argv[1], 'gpu-operator', versions)
