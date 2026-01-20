#!/bin/bash

IMAGE="felbus/hawkflow:remdingo-app"
CONTAINER="remdingo-app"
PORT="5814:5814"

echo "Updating $CONTAINER..."
sudo docker pull "$IMAGE"
sudo docker stop "$CONTAINER"
sudo docker rm "$CONTAINER"
sudo docker run --restart=always -e REMDINGO_ENVIRONMENT=production -p "$PORT" --name "$CONTAINER" -d "$IMAGE"
echo "$CONTAINER updated successfully!"

