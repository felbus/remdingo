#!/bin/bash

py=$(python -c 'import sys; print(sys.version_info[:])')

if [[ $py != "(3, 11, 1, 'final', 0)" ]]; then
  echo "You are not in the correct python environment"
  exit
fi

function remove_remdingo_docker() {
  docker stop remdingo-postgres
  docker stop remdingo-app

  sleep 5;

  docker rm remdingo-postgres
  docker rm remdingo-app
  docker rmi remdingo-app
  docker rmi remdingo-postgres
  
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

function remdingo_postgres_schema() {
  cd remdingo/app || exit

  echo ''
  echo '*** postgres schema ***'
  echo ''
  for i in {1..5}; do flask resetdb && break || sleep 5; done

  cd ../..
}

remove_remdingo_docker
create_remdingo_volumes
clean_remdingo_volumes
run_compose
remdingo_postgres_schema

