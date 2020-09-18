#!/bin/sh

set -e

echo "Check whether submodule commits are on their corresponding master branches."
git submodule foreach "git branch --all --format '%(refname:lstrip=-1)' --contains | grep -q '^master$'"
