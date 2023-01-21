#!/bin/bash

py=$(python -c 'import sys; print(sys.version_info[:])')

if [[ $py != "(3, 11, 1, 'final', 0)" ]]; then
  echo "You are not in the correct python environment"
  exit
fi

function remove_remdingo_docker() {
  docker stop remdingo-postgres 

  sleep 5;

  docker rm remdingo-postgres
  
  sleep 3;
}

function create_remdingo_volumes() {
  echo ''
  echo 'ensure volumes exist'
  mkdir -p ~/docker/volumes/remdingo/*
}

function clean_remdingo_volumes() {
  echo 'remove docker volumes'
  rm -fr ~/docker/volumes/remdingo/*
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
create_remdingo_volumes
clean_remdingo_volumes
run_compose

