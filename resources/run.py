import docker
import time
import requests
import sys
import subprocess

from config import workspace_name, workspace_port, network_name

client = docker.from_env()
try:
    client.networks.get(network_name)
except docker.errors.NotFound:
    client.networks.create(network_name, driver='bridge')

container = client.containers.run(
    'mltooling/ml-workspace-minimal:0.9.1',
    network=network_name,
    name=workspace_name,
    environment={
        "WORKSPACE_NAME": workspace_name
    },
    detach=True)

index = 0
health_url = f'http://{workspace_name}:{workspace_port}/healthy'
r = None
while r == None or (r.status_code != 200 and index < 15):
    index+=1
    time.sleep(1)
    try:
        r = requests.get(health_url, allow_redirects=False, timeout=2)
    except requests.ConnectionError as e:
        # Catch error that is raised when the workspace container is not reachable yet
        pass
    print(f"Try {index}", flush=True)

if index == 15:
    # The workspace did not start
    sys.exit(-1)

exit_code = 0
# Sleep a moment to give all processes time to start within the Workspace container
time.sleep(15)
print("Workspace started! Execute tests:", flush=True)
exit_code = subprocess.call(["python", "/resources/test.py"])
print("Executed tests.", flush=True)

# Cleanup
print("Clean up landscape", flush=True)
container.remove(force=True)

sys.exit(exit_code)
