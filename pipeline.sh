#!/bin/bash

chmod +x ./parallel_clone_repos.sh
chmod +x ./parallel_setup_repo_envs.sh
chmod +x ./parallel_run_tests.sh
chmod +x ./parallel_analyze_tests.sh

./parallel_clone_repos.sh
./parallel_setup_repo_envs.sh
./parallel_run_tests.sh
./parallel_analyze_tests.sh
