import json
from settings import settings

def generate_test_triggers(file_path=settings.new_version_file_path, output_file=settings.tests_to_trigger_file_path):
    # Read the JSON file
    with open(file_path, "r") as f:
        data = json.load(f)

    gpu_operator_versions = data.get("gpu-operator", {})
    ocp_versions = data.get("ocp", {})

    test_commands = set()

    # Generate test triggers for GPU operator versions
    for version in gpu_operator_versions:
        formatted_version = version.replace(".", "-")
        for ocp_version in ["4.12", "4.14", "4.15", "4.16", "4.17", "4.18"]:
            test_commands.add(f"/test {ocp_version}-stable-nvidia-gpu-operator-e2e-{formatted_version}-x")

    # Generate test triggers for OCP versions
    for ocp_version in ocp_versions:
        for gpu_version in ["24.6", "24.9", "master"]:
            formatted_version = gpu_version if gpu_version == "master" else gpu_version.replace(".", "-") + "-x"
            test_commands.add(f"/test {ocp_version}-stable-nvidia-gpu-operator-e2e-{formatted_version}")

    # Write unique test commands to output file
    with open(output_file, "w") as f:
        for command in sorted(test_commands):
            f.write(command + "\n")

if __name__ == "__main__":
    generate_test_triggers()
