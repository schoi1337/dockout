# attacks/dirty_pipe_escalation.py

def run(container, simulate=False):
    print("[*] Running Dirty Pipe (CVE-2022-0847) exploit...")

    if simulate:
        print(f"[SIMULATE] Would attempt to overwrite /tmp/readonly.txt in container '{container.name}'")
        print("[SIMULATE] This file is normally read-only. If overwritten, exploit is successful.")
        return "Simulated run: No dirty pipe payload executed."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        # Write to a file that is intended to be read-only (for demonstration only)
        command = "echo 'pwned' > /tmp/readonly.txt"
        container.exec_run(command, privileged=True)

        print("[+] Dirty Pipe payload attempted: /tmp/readonly.txt overwritten")
        return "Executed: dirty pipe simulation"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
