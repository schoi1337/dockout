# Path: docker/dev_targets/cve_2019_5736/Dockerfile

FROM ubuntu:20.04

# Suppress interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Install basic CLI tools required for exploit and validation
RUN apt update && apt install -y bash coreutils curl

# Create a marker file to validate pre-exploit state
RUN echo "LEGIT SHELL" > /LEGIT_MARKER

# Leave /bin/sh pointing to the original bash binary
# The exploit will overwrite /bin/sh → /tmp/pwned_shell.sh during execution

CMD ["bash"]
