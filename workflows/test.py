#!/usr/bin/env python

import logging
import re
import sys
import semver
import requests

from utils import update_key

logger = logging.getLogger('update_version')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
QUAY_API_URL = "https://quay.io/api/v1/repository/openshift-release-dev/ocp-release/tag/"
ocp_stable_version = ["4.12", "4.14" ,"4.15" ,"4.16" ,"4.17" ,"4.18","4.19", "4.20"]


def get_latest_ocp_patch_version():
    latest_versions = []
    for version in ocp_stable_version:
        versions = []
        params = {
            "filter_tag_name": f"like:{version}.%",
        }
        response = requests.get(QUAY_API_URL, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return None
        data = response.json()
        for tag in data.get("tags", []):
            tag_name: str = tag.get("name", "")
            match = re.match(rf"^{version}\.(\d+)-x86_64$", tag_name)
            if match:
                versions.append(tag_name.removesuffix("-x86_64"))
            else:
                match = re.match(rf"^{version}\.0-ec\.(\d+)-x86_64$", tag_name)
                if match:
                    versions.append(tag_name.removesuffix("-x86_64"))

        if not versions:
            print(f"No versions found for {version}")
            continue

        latest_version = max(sorted(versions, key=semver.VersionInfo.parse))
        latest_versions.append(latest_version)
    return latest_versions


if __name__ == '__main__':
    latest_versions = get_latest_ocp_patch_version()
    for version in latest_versions:
        match = re.match(r"(\d+\.\d+)", version)
        v = match.group(1)
        update_key(sys.argv[1], v, version)
