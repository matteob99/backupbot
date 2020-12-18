#!/usr/bin/env bash
if [ "${{ matrix.database }}" != influxdb ]; then
  declare -a archs=("linux386" "linuxamd64" "linuxarmv6" "linuxarmv7" "linuxarm64" "linuxppc64le")
else
  declare -a archs=("linuxamd64" "linuxarmv7" "linuxarm64" "linuxppc64le")
fi
# -- Push to ghcr.io
manifest=""
for arch in "${archs[@]}"; do
   manifest="$manifest --amend ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }}-$arch"
done
docker manifest create ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }} "$manifest"
docker manifest push ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }}

# Tag images as VERSION (like 'latest')
for arch in "${archs[@]}"; do
  docker tag "${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }}-$arch" "${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.VERSION }}-$arch"
done
manifest=""
for arch in "${archs[@]}"; do
   manifest="$manifest --amend ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.VERSION }}-$arch"
done
docker manifest create ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.VERSION }} "$manifest"
docker manifest push ${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.VERSION }}

# -- PUsh to Docker Hub
for arch in "${archs[@]}"; do
  docker tag "${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }}-$arch" "${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.VERSION }}-$arch"
done
manifest=""
for arch in "${archs[@]}"; do
   manifest="$manifest --amend ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.HASH_VERSION }}-$arch"
done
docker manifest create ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.HASH_VERSION }} "$manifest"
docker manifest push ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.HASH_VERSION }}
# Tag images as VERSION (like 'latest')
for arch in "${archs[@]}"; do
  docker tag "${{ env.IMAGE_TAG }}:${{ matrix.database }}-${{ env.HASH_VERSION }}-$arch" "${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.VERSION }}-$arch"
done
manifest=""
for arch in "${archs[@]}"; do
   manifest="$manifest --amend ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.VERSION }}-$arch"
done
docker manifest create ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.VERSION }} "$manifest"
docker manifest push ${{ env.IMAGE_TAG_DH }}:${{ matrix.database }}-${{ env.VERSION }}
