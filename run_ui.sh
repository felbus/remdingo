#!/bin/bash

py=$(python -c 'import sys; print(sys.version_info[:])')

if [[ $py != "(3, 11, 1, 'final', 0)" ]]; then
  echo "You are not in the correct python environment"
  exit
fi

function remove_remdingo_docker() {
  docker stop remdingo-app

  sleep 5;

  docker rm remdingo-app
  docker rmi remdingo-app

  sleep 3;
}

function run_compose() {
  echo ''
  echo '*** running docker compose ***'
  echo ''
  docker-compose up -d
  sleep 5;
}

remove_remdingo_docker
run_compose

