# Path: docker/dev_targets/cve_2019_5736/Dockerfile

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install basic tools
RUN apt update && apt install -y bash coreutils curl

# 공격 전 확인용 파일
RUN echo "LEGIT SHELL" > /LEGIT_MARKER

# 기본적으로 /bin/sh는 bash 바이너리 그대로 유지
# 나중에 공격 시 PoC에서 /bin/sh → /tmp/pwned_shell.sh 로 overwrite 함

CMD ["bash"]
