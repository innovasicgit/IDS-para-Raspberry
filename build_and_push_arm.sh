#!/bin/bash
# Build and push ARM image for IDS app
docker buildx build --platform linux/arm64 -t juancaing/ids-iot-app:arm . --push
