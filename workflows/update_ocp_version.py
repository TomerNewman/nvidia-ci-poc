#!/usr/bin/env python

import sys
import requests
from utils import update_key, get_logger
from settings import settings

logger = get_logger()

def fetch_ocp_versions():
    versions = []
    page_size :int = 100
    has_more :bool = True
    tag_filter :str = "like:4.1%.%-multi-x86_64"
    page :int = 1

    while has_more:
        response = requests.get(settings.quay_url_api, params={
            "limit": str(page_size), "page": page, "filter_tag_name": tag_filter, "onlyActiveTags": "true"})
        response.raise_for_status()
        response_json = response.json()
        has_more = response_json.get("has_additional")
        page = page + 1

        for tag in response_json.get("tags", []):
            tag_name = tag.get("name", "")
            match = settings.tag_regex.match(tag_name)
            if match:
                versions.append(match.group("version"))

    return versions

def get_latest_ocp_patch_versions():
    latest_versions = {}
    versions = fetch_ocp_versions()
    # if versions:
    #     latest_version = max(versions, key=semver.VersionInfo.parse)
    #     latest_versions[version] = latest_version

    return latest_versions

if __name__ == '__main__':
    versions = get_latest_ocp_patch_versions()
    update_key(sys.argv[1], "ocp", versions)

