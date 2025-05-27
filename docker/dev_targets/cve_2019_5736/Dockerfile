# docker/dev_targets/cve_2019_5736/Dockerfile

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y bash coreutils curl

# Create original shell that outputs "LEGIT SHELL"
RUN echo -e '#!/bin/bash\necho "LEGIT SHELL"' > /tmp/original_shell.sh && chmod +x /tmp/original_shell.sh

# Replace /bin/sh with symbolic link to controlled shell
RUN ln -sf /tmp/original_shell.sh /bin/sh

CMD ["bash"]
