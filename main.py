import subprocess

import subprocess

def run_command(command):
    """Executes the given command and returns the output, providing detailed logging."""
    try:
        print(f"Executing command: {command}")
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print("Command success. Output:")
        print(output.decode('utf-8'))
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.output.decode('utf-8'))
        return ""

def patch_or_clear_namespace_selector(namespace, selector=None):
    """Patches or clears the node-selector annotation on the namespace, with debugging information."""
    if selector:
        print(f"Applying node selector '{selector}' to namespace '{namespace}'")
        run_command(f"oc patch namespace {namespace} -p '{{\"metadata\": {{\"annotations\": {{\"openshift.io/node-selector\": \"{selector}\"}}}}}}'")
    else:
        print(f"Clearing node selector from namespace '{namespace}'")
        run_command(f"oc patch namespace {namespace} -p '{{\"metadata\": {{\"annotations\": {{\"openshift.io/node-selector\": null}}}}}}'")


def fetch_current_group_memberships(groups):
    """Fetches current users for each provided group, with debugging information."""
    memberships = {}
    for group in groups:
        print(f"Fetching members for group: {group}")
        memberships[group] = run_command(f"oc get groups {group} -o jsonpath='{{.users[*]}}'").split()
        print(f"Members in {group}: {memberships[group]}")
    return memberships

def fetch_user_namespaces(user):
    """Fetches namespaces where the given user is the requester, with debugging information."""
    print(f"Fetching namespaces for user: {user}")
    # Correct JSONPath expression using proper notation
    # Ensure the JSONPath expression is enclosed in single quotes and use the correct filter syntax
    command = f"oc get projects -o=json | jq -r '.items[] | select(.metadata.annotations.\"openshift.io/requester\"==\"{user}\") | .metadata.name'"
    namespaces = run_command(command).strip().split()
    print(f"Namespaces owned by {user}: {namespaces}")
    return namespaces

# Define groups and node selectors
groups = ["NVIDIA_VPU_LS40S", "NVIDIA_TESLA_V100_PCIE_16GB"]
selectors = {
    "NVIDIA_VPU_LS40S": "nvidia.com/gpu.product=NVIDIA-L40S",
    "NVIDIA_TESLA_V100_PCIE_16GB": "nvidia.com/gpu.product=Tesla-V100-PCIE-16GB",
    "BOTH": "allow-l40s-and-v100=true",
    "NONE": "nogpu=true"
}

# Main logic to update namespace annotations based on group memberships
current_memberships = fetch_current_group_memberships(groups)
all_users = set(sum(current_memberships.values(), []))  # Flatten list to get a set of unique users

for user in all_users:
    user_groups = {group for group, users in current_memberships.items() if user in users}
    print(f"User {user} is in groups: {user_groups}")
    user_namespaces = fetch_user_namespaces(user)
    
    if "NVIDIA_VPU_LS40S" in user_groups and "NVIDIA_TESLA_V100_PCIE_16GB" in user_groups:
        node_selector = selectors["BOTH"]
    elif "NVIDIA_VPU_LS40S" in user_groups:
        node_selector = selectors["NVIDIA_VPU_LS40S"]
    elif "NVIDIA_TESLA_V100_PCIE_16GB" in user_groups:
        node_selector = selectors["NVIDIA_TESLA_V100_PCIE_16GB"]
    else:
        node_selector = None
    
    print(f"Node selector for {user}: {node_selector if node_selector else 'No GPU access'}")
    
    for namespace in user_namespaces:
        patch_or_clear_namespace_selector(namespace, node_selector)
