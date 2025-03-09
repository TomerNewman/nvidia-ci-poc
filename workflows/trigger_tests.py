import json
from pickle import format_version

from settings import settings
from utils import get_latest_versions_to_test


def generate_test_triggers():
    with open(settings.full_versions_file_path, "r") as f:
        all_data = json.load(f)

    latest_gpu_versions, latest_ocp_versions = get_latest_versions_to_test(all_data)

    with open(settings.diff_version_file_path, "r") as f:
        data = json.load(f)

    gpu_operator_versions = data.get("gpu-operator", {})
    ocp_versions = data.get("ocp", {})
    bundle_image = data.get("gpu-main-latest", "")

    test_commands = set()

    if bundle_image != "":
        for version in latest_ocp_versions:
            test_commands.add(f"/test {version}-stable-nvidia-gpu-operator-e2e-master")

    for version in gpu_operator_versions:
        if version not in latest_gpu_versions: # commenting only changed latest gpu versions
            continue
        formatted_version = version.replace(".", "-")
        for ocp_version in latest_ocp_versions:
            test_commands.add(f"/test {ocp_version}-stable-nvidia-gpu-operator-e2e-{formatted_version}-x")

    for ocp_version in ocp_versions:
        for gpu_version in latest_gpu_versions:
            formatted_version = gpu_version if gpu_version == "master" else gpu_version.replace(".", "-") + "-x"
            test_commands.add(f"/test {ocp_version}-stable-nvidia-gpu-operator-e2e-{formatted_version}")

    with open(settings.tests_to_trigger_file_path, "w") as f:
        for command in sorted(test_commands):
            f.write(command + "\n")



if __name__ == "__main__":
    generate_test_triggers()
