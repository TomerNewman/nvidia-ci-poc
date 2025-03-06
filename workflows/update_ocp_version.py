#!/usr/bin/env python

import sys
import semver
import requests
from utils import update_key, get_logger
from settings import settings

logger = get_logger()

def fetch_ocp_versions(version: str):
    versions = []
    params = {"filter_tag_name": f"like:{version}.%"}

    try:
        response = requests.get(settings.quay_url_api, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data for {version}: {e}")
        return []

    for tag in response.json().get("tags", []):
        tag_name = tag.get("name", "")
        match = settings.tag_regex.match(tag_name)
        if match:
            versions.append(match.group("version"))

    if not versions:
        logger.warning(f"no versions found for {version}")

    return versions

def get_latest_ocp_patch_versions():
    latest_versions = []

    for version in settings.tracked_versions:
        versions = fetch_ocp_versions(version)
        if versions:
            latest_version = max(versions, key=semver.VersionInfo.parse)
            latest_versions.append(latest_version)

    return latest_versions

if __name__ == '__main__':
    versions = get_latest_ocp_patch_versions()
    for latest_version in versions:
        major_minor_key = latest_version.rsplit(".", 1)[0]
        update_key(sys.argv[1], major_minor_key, latest_version)
        logger.info(f"updated {sys.argv[1]}: {major_minor_key} -> {latest_version}")
