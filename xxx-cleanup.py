import subprocess

def run_command(command):
    """Executes the given command and prints the output, handling errors."""
    try:
        print(f"Executing command: {command}")
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print("Command success. Output:")
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.output.decode('utf-8'))

def remove_user_from_groups(user, groups):
    """Removes a user from specified groups."""
    for group in groups:
        print(f"Removing user {user} from group {group}...")
        run_command(f"oc adm groups remove-users {group} {user}")

def delete_project(project_name):
    """Deletes a specified project."""
    print(f"Deleting project {project_name}...")
    run_command(f"oc delete project {project_name}")

def delete_user(user):
    """Deletes a specified user."""
    print(f"Deleting user {user}...")
    run_command(f"oc delete user {user}")

def delete_group(group):
    """Deletes a specified group."""
    print(f"Deleting group {group}...")
    run_command(f"oc delete group {group}")

# Define the users, their groups, and their projects
user_groups = {
    "ajones": ["NVIDIA_VPU_LS40S"],
    "bjohnson": ["NVIDIA_VPU_LS40S"],
    "csmith": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "dwilliams": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "hwhite": ["NVIDIA_VPU_LS40S", "NVIDIA_TESLA_V100_PCIE_16GB"],
    "ijackson": ["NVIDIA_TESLA_V100_PCIE_16GB"],
    "bpandey": ["NVIDIA_VPU_LS40S", "NVIDIA_TESLA_V100_PCIE_16GB"]
}

user_projects = {
    "ajones": ["ajones-project1", "ajones-project2", "ajones-project3"],
    "bjohnson": ["bjohnson-project1", "bjohnson-project2"],
    "csmith": ["csmith-project1", "csmith-project2"],
    "dwilliams": ["dwilliams-project1", "dwilliams-project2"],
    "hwhite": ["hwhite-project1", "hwhite-project2"],
    "ijackson": ["ijackson-project1", "ijackson-project2"],
    "bpandey": ["bpandey-project1"]
}

# Remove users from their groups
for user, groups in user_groups.items():
    remove_user_from_groups(user, groups)

# Delete projects for each user
for user, projects in user_projects.items():
    for project in projects:
        delete_project(project)

# Delete the users
for user in user_groups.keys():
    delete_user(user)

# Delete the groups
for group in set(group for groups in user_groups.values() for group in groups):
    delete_group(group)