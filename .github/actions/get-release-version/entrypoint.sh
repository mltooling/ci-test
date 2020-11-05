#!/bin/bash

# Stops script execution if a command has an error
set -e

BRANCH_NAME=$(git branch --show-current)

echo $(git branch --show-current)
if [ -z $INPUT_BRANCH_PREFIX ]; then
    INPUT_BRANCH_PREFIX=""
fi

if [[ ! $BRANCH_NAME == $INPUT_BRANCH_PREFIX* ]]; then
    echo "Branch $BRANCH_NAME does not start with prefix $INPUT_BRANCH_PREFIX"
    exit 1
fi

# Remove prefix from version
RELEASE_VERSION="${BRANCH_NAME#$INPUT_BRANCH_PREFIX}"

if [[ ! "$RELEASE_VERSION" =~ ^v([0-9]+\.[0-9]+\.[0-9]+.*)$ ]]; then
    echo "The branch does not contain a valid version: $RELEASE_VERSION"
    exit 1
fi

# Remove v from version string
RELEASE_VERSION=$(echo $RELEASE_VERSION | sed -E 's/v([0-9]+\.[0-9]+\.[0-9]+.*)/\1/')

# Set version as outpu
echo "::set-output name=release_version::$RELEASE_VERSION"
