# Dockout – Docker Escape Automation Tool

## Author
schoi1337

## License
MIT

## Category
Exploitation Tools

## Description
Dockout is a red-team–focused framework that automates detection and exploitation of container breakout vulnerabilities.  
It supports safe simulation (`--simulate`) as well as real-world exploitation (`--unsafe`) with interactive prompts.  
Each module is plugin-based and covers common CVEs such as CVE-2019-5736 and OverlayFS.

## Features
- Plugin-based attack modules loaded from `attacks/`
- Real or simulated exploit execution
- CLI interface with full flag-based control
- HTML/JSON report generation with risk level and recommendations
- Menu integration via `.desktop` file
- Custom icon included (`icon.png`)

## Usage
```bash
python3 src/core.py --auto --simulate --container demo-container
```

## Notes
This tool includes metadata and assets prepared for submission to Kali Linux.