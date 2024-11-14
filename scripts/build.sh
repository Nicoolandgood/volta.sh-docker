#!/bin/bash

docker buildx build . --platform linux/amd64,linux/arm64,linux/arm --tag nicoolandgood/volta.sh:latest --push
