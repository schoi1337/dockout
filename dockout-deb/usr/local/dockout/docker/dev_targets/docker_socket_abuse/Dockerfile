# docker/dev_targets/docker_socket_abuse/Dockerfile

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y curl jq

# This image is intended to test Docker socket abuse
# Make sure to run it with the Docker socket mounted:
# docker run -dit --name test-container -v /var/run/docker.sock:/var/run/docker.sock docker-socket-test

CMD ["bash"]
