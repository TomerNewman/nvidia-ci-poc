import json
import logging
import semver

from typing import Tuple
from settings import settings


def update_key(versions_file, version_key, version_value):
    logger = get_logger()
    with open(versions_file, "r+") as json_f:
        data = json.load(json_f)
        old_version = data.get(version_key)
        if old_version == version_value:
            logger.info('No changes detected, exit')
            return

        logger.info(f'New version detected: {version_value} (was {old_version})')

        data[version_key] = version_value
        json_f.seek(0)  # rewind
        json.dump(data, json_f, indent=4)
        json_f.truncate()

    with open(settings.diff_version_file_path, "r+") as json_f:
        data = json.load(json_f)
        data[version_key] = version_value

        json_f.seek(0)  # rewind
        json.dump(data, json_f, indent=4)
        json_f.truncate()


def get_logger():
    logger = logging.getLogger('update_version')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_two_highest_gpu_versions(gpu_versions: dict):
    sorted_versions = sorted(gpu_versions.keys(), key=lambda v: tuple(map(int, v.split('.'))), reverse=True)
    return sorted_versions[:2]


def get_latest_versions_to_test(data: dict) -> Tuple[list[str], list[str]]:
    all_ocp_versions = data.get("ocp", {})

    all_gpu_operator_versions = data.get("gpu-operator", {})
    latest_gpu_versions = get_two_highest_gpu_versions(all_gpu_operator_versions)
    latest_gpu_versions.append("master")
    return latest_gpu_versions, list(all_ocp_versions.keys()) # returning list of latest ocp + gpu versions
