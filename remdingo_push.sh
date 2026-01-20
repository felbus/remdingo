#!/bin/bash

app() {
  docker buildx build --platform linux/amd64 --no-cache -t remdingo-app -f Dockerfile.app . --load
  docker tag remdingo-app felbus/hawkflow:remdingo-app
  docker push felbus/hawkflow:remdingo-app
}

help()
{
   echo "Push remdingo container to docker hub."
   echo
   echo "options:"
   echo "--app   Push the remdingo app container"
   echo
}

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      --app)
        echo 'pushing remdingo app'
        app
        exit;;
      \?)
         echo "Error: Invalid option"
         exit;;
   esac
done
