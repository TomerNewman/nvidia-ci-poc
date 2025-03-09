#!/usr/bin/env python

import requests
import semver
import sys
from utils import update_key, get_logger
from settings import settings

logger = get_logger()

def fetch_ocp_versions():
    versions = {}
    page_size :int = 100
    has_more :bool = True
    tag_filter :str = "like:%.%.%-multi-x86_64"
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
            if not match:
                continue

            minor = match.group("minor")
            if minor in settings.ignored_versions:
                continue

            full = f"{minor}.{match.group("patch")}"
            patches = versions.get(minor)
            versions[minor] = semver.max_ver(versions[minor], full) if patches else full

    return versions

if __name__ == '__main__':
    versions = fetch_ocp_versions()
    update_key(sys.argv[1], "ocp", versions)
