
## AnyLog Versions
AnyLog has 3 major versions, each version is built on both _Ubuntu:20.04_ with _python:3.9-alpine_. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. 
Usually the image will be Ubuntu based, unless stated otherwise.


| Build             | Base Image          | CPU Architecture | Pull Command                                            | Compressed Size | 
|-------------------|---------------------|---|---------------------------------------------------------|-----------------|
| develop           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop`           | ~320MB                | 
| develop-alpine    | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine`    | ~170MB                |
| develop-rhl       | redhat/ubi8:latest  | amd64,arm64 | `docker pull anylogco/anylog-network:develop-rhl`       |  ~215MB               |
| predevelop        | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop`        | ~320MB          | 
| predevelop-alpine | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~170MB          |
| predevelop-rhl    | redhat/ubi8:latest   | amd64,arm64 | `docker pull anylogco/anylog-network:predevelop-rhl`    | ~215MB          |
| testing           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:testing`           |

*Compressed Size - size calculated by summing the image's compressed layers size.