docker build --pull -t "$CI_REGISTRY_IMAGE:postgresql" --build-arg database=postgresql  .
docker build --pull -t "$CI_REGISTRY_IMAGE:mariadb" --build-arg database=mariadb  .
docker build --pull -t "$CI_REGISTRY_IMAGE" --build-arg database=postgresql  .
docker push "$CI_REGISTRY_IMAGE:postgresql"

docker push "$CI_REGISTRY_IMAGE"

docker push "$CI_REGISTRY_IMAGE:mariadb"