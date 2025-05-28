# 🐳 Dockout Installation Guide

This document explains how to install and test Dockout on Kali Linux.  
It includes both simulated and real-world test environments using Docker containers.

## 🧰 Prerequisites

- Kali Linux (2025.1 or later recommended)
- Python 3.9+ (default on Kali)
- Docker

Install dependencies:

```bash
sudo apt update
sudo apt install -y docker.io 
sudo systemctl start docker
sudo systemctl enable docker
```

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/schoi1337/dockout.git
cd dockout
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## 🧪 Testing with Dev Containers

Dockout provides ready-to-use vulnerable Dockerfiles under `docker/dev_targets/`.

### Example: CVE-2019-5736

```bash
# Build the test container
sudo docker build -t cve-2019-5736-vuln docker/dev_targets/cve_2019_5736

# Run it with unrestricted syscall access (required for exploit)
sudo docker run -it --rm --name test-cve \
  --security-opt seccomp=unconfined \
  cve-2019-5736-vuln
```

> 🧠 **Note:** The `--security-opt seccomp=unconfined` flag disables syscall filtering to allow full exploit behavior. This is necessary for certain PoCs such as CVE-2019-5736 that overwrite runtime binaries.

You can repeat this with other targets:
- `cve_2021_3156`
- `dirty_pipe_escalation`
- `docker_socket_abuse`
- `overlayfs_exploit`

## 🚀 Run Dockout (Simulated Mode)

From another terminal, run:

```bash
python3 src/core.py --auto --simulate --container test-cve --report html
```

This will simulate all applicable exploits and generate reports:

- `reports/attack_report.html`
- `reports/attack_report.json`

## 🔥 Real Exploit Mode (Unsafe)

To execute real container escape exploits:

```bash
python3 src/core.py --auto --unsafe --container test-cve --report html
```

>⚠️ **Warning:** This may overwrite files inside the container or cause system instability. Only use in isolated test environments.

## 🧾 Sample Report

A sample HTML report is included at:

```
docs/sample_report.html
```

## 🖥️ Desktop Integration (Optional)

- App launcher: `dockout.desktop`
- Icon: `icon.png`

## 📫 Contact

For questions, visit:[https://github.com/schoi1337/dockout/issues](https://github.com/schoi1337/dockout/issues)