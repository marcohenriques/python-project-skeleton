#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

echo "Running: '$cmd'"
exec $cmd
