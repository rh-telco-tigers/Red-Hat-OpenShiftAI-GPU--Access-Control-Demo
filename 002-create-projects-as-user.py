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

def create_project_for_user(username, project_name):
    """Creates a project for a given user."""
    print(f"Creating project {project_name} for user {username}...")
    run_command(f"oc new-project {project_name} --as={username}")

# Define users and their respective projects using a dictionary
user_projects = {
    "ajones": ["ajones-project1", "ajones-project2", "ajones-project3"],
    "bjohnson": ["bjohnson-project1", "bjohnson-project2"],
    "csmith": ["csmith-project1", "csmith-project2"],
    "dwilliams": ["dwilliams-project1", "dwilliams-project2"],
    "hwhite": ["hwhite-project1", "hwhite-project2"],
    "ijackson": ["ijackson-project1", "ijackson-project2"],
    "bpandey": ["bpandey-project1"]
}

# Create projects for each user based on the dictionary
for user, projects in user_projects.items():
    for project in projects:
        create_project_for_user(user, project)