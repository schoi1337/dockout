FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y sudo perl

# Add a dummy user with passwordless sudo (for sudoedit test)
RUN useradd -m testuser && echo 'testuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER testuser
WORKDIR /home/testuser

CMD ["bash"]
