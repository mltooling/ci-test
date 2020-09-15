import docker
import time

client = docker.from_env()

container = client.containers.run(
    'mltooling/ml-workspace-minimal:0.9.1 ',
    network="ci-test-net",
    hostname="workspace"
    detach=True)

index = 0

while index < 15:
    index+=1
    time.sleep(1)
