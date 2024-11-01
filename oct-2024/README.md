# Build Instructions

```
docker buildx build -f docker/Dockerfile1 --push --tag russellsaerang/csit-oct-2024:part1 .
docker buildx build -f docker/Dockerfile2 --push --tag russellsaerang/csit-oct-2024:part2 .
```

# Usage

```
docker run -it russellsaerang/csit-oct-2024:part1
docker run -it russellsaerang/csit-oct-2024:part2
```