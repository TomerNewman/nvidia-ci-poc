import json
import logging

logger = logging.getLogger('versions')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def update_key(versions_file, version_key, version_value):

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

def update_keys(versions_file, group_key, values):

    with open(versions_file, "r+") as json_f:
        data = json.load(json_f)
        old_versions = data.get(group_key)
        if old_versions == values:
            logger.info('No changes detected, exit')
            return

        logger.info(f'Changes detected: {values} (was {old_versions})')
        data[group_key] = values
        json_f.seek(0)  # rewind
        json.dump(data, json_f, indent=4)
        json_f.truncate()