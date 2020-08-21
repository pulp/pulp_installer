#!/bin/bash

function run_ansible_lint {
    base_dir=$(dirname "$(readlink -f "$0")")
    cd $base_dir/../
    roles_dirs=($(find . -maxdepth 1 -name roles -not -path "*ansible_collections*" -not -path "./tar-build/*"))
    role_dirs=( )

    for i in "${roles_dirs[@]}"
    do
        role_dirs+=($(find $i -maxdepth 1))
    done

    ansible-lint -t file -r $base_dir/ansible_lint_rules "${role_dirs[@]}"
}

run_ansible_lint
