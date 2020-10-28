#!/bin/bash

# Stops script execution if a command has an error
set -e

printenv

ADDITIONAL_OPTIONS=""

if [[ $INPUT_CURRENT_COMMIT_ONLY = true ]] ; then
    ADDITIONAL_OPTIONS="--exact-match"
fi

LATEST_VERSION=$(git describe --tags --match 'v[0-9].*' --abbrev=0 $ADDITIONAL_OPTIONS)
# LATEST_VERSION="git tag --points-at HEAD --sort -version:refname | head -1"
# --exact-match

if [[ ! "$LATEST_VERSION" =~ ^v([0-9]+\.[0-9]+\.[0-9]+.*)$ ]] ; then
    echo "The latest tag is not valid: $LATEST_VERSION"
    exit 1
fi

LATEST_VERSION=$(echo $LATEST_VERSION | sed -E 's/v([0-9]+\.[0-9]+\.[0-9]+.*)/\1/')

echo "::set-output name=version::$LATEST_VERSION"
echo "::set-env name=LATEST_VERSION::$LATEST_VERSION"
