import subprocess

def run_command(command):
    """Runs a shell command and returns the output, logging the command and its result."""
    try:
        print(f"Executing command: {command}")
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print("Command success. Output:")
        print(output.decode('utf-8'))
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.output.decode('utf-8'))
        return e.output.decode('utf-8')

# Redefined dictionary to ensure unique association of nodes and labels
node_labels = {
    "master1.cloud9c.xxx.dfw.ocp.run": ["nogpu=true"],
    "master2.cloud9c.xxx.dfw.ocp.run": ["nvidia.com/gpu.product=Tesla-V100-PCIE-16GB", "allow-l40s-and-v100=true"],
    "master3.cloud9c.xxx.dfw.ocp.run": ["nvidia.com/gpu.product=NVIDIA-L40S", "allow-l40s-and-v100=true"]
}

# Apply labels to nodes using the updated dictionary
for node, labels in node_labels.items():
    for label in labels:
        command = f"oc label node {node} {label} --overwrite"
        run_command(command)