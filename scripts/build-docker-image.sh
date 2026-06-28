#!/bin/bash

set -euo pipefail

source .env

ros_distro="${ROS_DISTRO:-lyrical}"
docker_image_version="${DOCKER_IMAGE_VERSION:-latest}"

local_image_name="ros-${ros_distro}-builder"
image_name="${IMAGE_NAME:-${local_image_name}}"

repo_full_name="${GITHUB_REPOSITORY:-unknown/unknown}"
git_sha="${GITHUB_SHA:-$(git rev-parse HEAD 2>/dev/null || echo unknown)}"

docker build \
    -t "${image_name}:${docker_image_version}" \
    --build-arg UID="$(id -u)" \
    --build-arg GID="$(id -g)" \
    --build-arg USER="$(whoami)" \
    --label "org.opencontainers.image.title=${local_image_name}" \
    --label "org.opencontainers.image.description=ROS ${ros_distro} builder image for local development and GitHub Actions CI" \
    --label "org.opencontainers.image.source=https://github.com/${repo_full_name}" \
    --label "org.opencontainers.image.revision=${git_sha}" \
    --label "org.opencontainers.image.version=${docker_image_version}" \
    .