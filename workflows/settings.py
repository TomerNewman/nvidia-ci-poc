import json
import os
import re
from typing import Pattern, AnyStr


class Settings:
    quay_url_api: str
    tag_regex: Pattern[AnyStr]
    ignored_versions: list[str]
    new_version_file_path: str
    tests_to_trigger_file_path: str

    def __init__(self):
        self.quay_url_api = os.getenv("OCP_TAGS_URL")
        self.tag_regex = re.compile(r"^(?P<version>\d+\.\d+\.\d+(?:-rc\.\d+)?)\-multi\-x86_64$")
        self.ignored_versions = json.loads(os.getenv("OCP_IGNORED_VERSIONS", "[]"))
        self.new_version_file_path = os.getenv("NEW_VERSION_FILE_PATH")
        self.tests_to_trigger_file_path = os.getenv("TEST_TO_TRIGGER_FILE_PATH")

settings = Settings()
