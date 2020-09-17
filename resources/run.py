import docker
import time
import requests
import sys
import subprocess

client = docker.from_env()
network_name = 'ci-test-net'
try:
    client.networks.get(network_name)
except docker.errors.NotFound:
    client.networks.create(network_name, driver='bridge')

name = "ci-test-workspace"
container = client.containers.run(
    'mltooling/ml-workspace-minimal:0.9.1',
    network=network_name,
    name=name,
    detach=True)

index = 0
health_url = f'http://{name}:8080/healthy'
r = None
while r == None or (r.status_code != 200 and index < 15):
    index+=1
    time.sleep(1)
    try:
        r = requests.get(health_url, allow_redirects=False, timeout=2)
    except requests.ConnectionError as e:
        # Catch error that is raised when the workspace container is not reachable yet
        pass
    print(f"Try {index}")

if index == 15:
    # The workspace did not start
    sys.exit(-1)

exit_code = 0
print("Workspace started! Execute tests:")
exit_code = subprocess.call(["python", "/resources/test.py"])
print("Executed tests.")

# Cleanup
print("Clean up landscape")
container.remove(force=True)

sys.exit(exit_code)
