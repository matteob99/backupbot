docker build --pull -t "$CI_REGISTRY_IMAGE:postgresql" --build-arg database=postgresql  .
docker build --pull -t "$CI_REGISTRY_IMAGE" --build-arg database=postgresql  .
docker build --pull -t "$CI_REGISTRY_IMAGE:mariadb" --build-arg database=mariadb  .
docker build --pull -t "$CI_REGISTRY_IMAGE:redis" --build-arg database=redis  .
docker build --pull -t "$CI_REGISTRY_IMAGE:influxdb" --build-arg database=influxdb  .
docker build --pull -t "$CI_REGISTRY_IMAGE:folder" --build-arg database=folder  .


docker push "$CI_REGISTRY_IMAGE:postgresql"
docker push "$CI_REGISTRY_IMAGE"
docker push "$CI_REGISTRY_IMAGE:mariadb"
docker push "$CI_REGISTRY_IMAGE:redis"
docker push "$CI_REGISTRY_IMAGE:influxdb"
docker push "$CI_REGISTRY_IMAGE:folder"