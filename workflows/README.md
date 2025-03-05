# Scripts and other files for automated workflows

## TODO

* Implement OpenShift versions
* Improve GPU operator releases - use `curl` or commit the Python libraries to avoid installing them every time
* Calculate the right tests to run for PR messages

## Useful links

* https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions
* https://stackoverflow.com/questions/70458458/how-do-i-simply-run-a-python-script-from-github-repo-with-actions
* https://github.com/marketplace/actions/create-pull-request

## Updating container images

* See https://docker-docs.uclv.cu/registry/spec/api/

### OpenShift releases

Public, doesn't require authentication, but requires pagination

```console
curl -SsL -X GET "https://quay.io/v2/openshift-release-dev/ocp-release/tags/list?n=100&last=4.18.0-x86_64" -H 'Content-Type: application/json'
```

### NVIDIA GPU operator (releases)

Public, but requires authentication (haven't figured out yet how to do it).
Maybe the Python SDK can give some clues https://docs.ngc.nvidia.com/sdk/index.html (or used directly).

The authentication should work along the lines of:

```console
export AUTH_TOKEN=$(echo '$ouathtoken:<ngc-api-key>' | base64 -w 0)
curl -vSsL 'https://authn.nvidia.com/token?service=ngc&group=ngc:kse5libxgpiz/no-team' -H "Authorization: Basic $AUTH_TOKEN" -H "Content-Type: application/json"
```

```console
curl -SsL -X GET https://nvcr.io/v2/nvidia/gpu-operator/tags/list -H 'Content-Type: application/json'
```

### NVIDIA GPU operator OLM bundle from main branch

Public, requires authentication. When running in a GitHub action, `secret.GITHUB_TOKEN` can be used to authentication.
See https://github.com/orgs/community/discussions/26279 and https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication

```console
token=$(curl -SsL https://ghcr.io/token\?scope\="repository:nvidia/gpu-operator:pull" | jq -r .token)

# listing tags
curl -SsL -X GET https://ghcr.io/v2/nvidia/gpu-operator/gpu-operator-bundle/tags/list -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" | jq

# getting the digest of `main-latest`
curl -SsL -X GET https://ghcr.io/v2/nvidia/gpu-operator/gpu-operator-bundle/manifests/main-latest -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" | jq -r .config.digest
```