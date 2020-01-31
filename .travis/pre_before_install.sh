#!/usr/bin/env bash

set -euv

if [[ $TOXENV == *"upgrade"* ]]; then
  docker pull quay.io/pulp/pulp-ci-c7:3.0.0
  docker pull quay.io/pulp/pulp-ci-dbuster:3.0.0
  docker pull quay.io/pulp/pulp-ci-f31:3.0.0
fi
