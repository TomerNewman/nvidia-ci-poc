import json
import logging

from settings import settings

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

    with open(settings.new_version_file_path, "r+") as json_f:

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