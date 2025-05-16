## Ansible playbook to Install / Update Microk8s

## Pre-requisite

1. Assuming Python already installed, in this case the playbook useing Python Version `3.10.13` adjust as needed
2. Install required python ansible on `requirement.txt`
3. Install ansible-galaxy of `community.general` to run snap command on ubuntu

## How to use

1. Update `hosts.ini` (required) file with your hostname, username private key and `ansible.cfg` (if needed)
2. Update the `microk8s_version` with the version you would like to install or update
3. Once updated, run with `ansible-playbook snap-update.yaml -e 'host_target=all' -K`
4. (Optional) put `-vvv` to debug whenever needed
5. Wait until the playbook finished
6. Check the k8s version with `kubernetes version`, the output should be similar to this output:

```
[22:11:49|25-05-16] 
Client Version: v1.33.0
Kustomize Version: v5.6.0
Server Version: v1.33.0
```
