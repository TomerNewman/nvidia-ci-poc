import re


class Settings:
    quay_url_api = "https://quay.io/api/v1/repository/openshift-release-dev/ocp-release/tag/"
    tag_regex = re.compile(r"^(?P<version>\d+\.\d+\.\d+(?:-ec\.\d+)?)\-x86_64$")
    tracked_versions = ["4.12", "4.14", "4.15", "4.16", "4.17", "4.18", "4.19", "4.20"]

settings = Settings()
