import subprocess

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(f"Executing: {command}")
        print("Success:", output.decode('utf-8'))
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Failed:", e.output.decode('utf-8'))
        return e.output.decode('utf-8')

def add_self_provisioner_role(username):
    """Assigns the self-provisioner role to a given user."""
    print(f"Assigning 'self-provisioner' role to user {username}...")
    run_command(f"oc adm policy add-cluster-role-to-user self-provisioner {username}")

# Create OpenShift groups
print("Creating OpenShift groups...")
run_command("oc adm groups new NVIDIA_VPU_LS40S")
run_command("oc adm groups new NVIDIA_TESLA_V100_PCIE_16GB")

# Define users and their respective groups using a dictionary
user_groups = {
    "ajones": ["NVIDIA_VPU_LS40S"],
    "bjohnson": ["NVIDIA_VPU_LS40S"],
    "csmith": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "dwilliams": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "hwhite": ["NVIDIA_VPU_LS40S", "NVIDIA_TESLA_V100_PCIE_16GB"],
    "ijackson": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "bpandey": ["NVIDIA_VPU_LS40S", "NVIDIA_TESLA_V100_PCIE_16GB"]
}

# Add users to their respective groups
for user, groups in user_groups.items():
    add_self_provisioner_role(user)
    for group in groups:
        print(f"Adding user {user} to group {group}...")
        run_command(f"oc adm groups add-users {group} {user}")

print("Group creation and user assignments complete.")
