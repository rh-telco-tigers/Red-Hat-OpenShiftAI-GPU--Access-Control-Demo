## Access Control for AcceleratorProfile
This project demonstrates a workaround solution to manage access control for the AcceleratorProfile, leveraging user group assignments in OpenShift environments—a capability not natively supported. Our method involves several key steps:

## Overview
Our approach enables controlled access to GPU resources by leveraging OpenShift's native capabilities to work with user groups and node labels. This ensures that only authorized users can access specific GPU types.

## Prerequisites
- OpenShift Cluster
- Access to OpenShift CLI
- Python 3.x

## Scripts Description

-  `001-create-user-and-groups.py`: This script creates dummy users and groups, assigning the self-provisioner role to each user to enable them to create their own projects.
- `002-create-project-as-user.py`: Runs under admin privileges to create dummy projects for testing purposes by impersonating users. This ensures that each project is associated with the correct user context.
- `003-add-node-labels.py`: Adds node labels for testing. These labels reflect the GPU types available and facilitate the selective access control based on user group associations.
- `main.py`: The main script that patches the namespaces created in step 2 based on user roles association. It configures node selectors within each project to restrict access to specific GPU resources.
- `xxx-cleanup.py`: Cleans up all dummy data created by the previous scripts. This script is essential for resetting the environment after tests are completed.

## Setup and Execution
1. Configure your OpenShift CLI: Ensure you are logged in as an administrator.
2. Run the Scripts:
```
python 001-create-user-and-groups.py
python 002-create-project-as-user.py
python 003-add-node-labels.py
python main.py
```
3. Cleanup:
```
python xxx-cleanup.py
```

## Contribution
Contributions to this project are welcome. You can enhance scripts, add automation features, or provide feedback for further improvements.



