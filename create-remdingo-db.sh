#!/bin/bash

# Create and run the remdingo postgres container
# This is a one-time script to create the database container

docker run -d --name remdingo-postgres -p 5435:5432 -v /data/volumes/remdingo:/var/lib/postgresql/data -e POSTGRES_PASSWORD=remdingo5435434 postgres:16

echo "remdingo-postgres container created"
echo "PostgreSQL is available at localhost:5435"

