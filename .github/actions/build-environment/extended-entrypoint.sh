echo "List Docker containers"
docker ps -a

echo "Inspect Docker container"
docker inspect $(hostname)

echo "Print GitHub Token"
echo $GITHUB_TOKEN

# Thereby, you can reuse the existing implementation:
/bin/bash /entrypoint.sh "$@"
# Save the exit code of the previous command
exit_code=$?

echo "Cleanup Phase"

# TODO: Do additional cleanup

# Exit the script with the exit code of the actual entrypoint execution
exit $exit_code
