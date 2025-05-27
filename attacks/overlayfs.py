# attacks/overlayfs_exploit.py

def run(container, simulate=False):
    print("[*] Running OverlayFS Exploit (CVE-2023-0386)...")

    if simulate:
        print(f"[SIMULATE] Would attempt to overwrite /overlayfs-test/target.txt inside '{container.name}'")
        print("[SIMULATE] Normally a read-only file would be replaced with attacker content.")
        return "Simulated run: No overlay modification done."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        # Overwrite a file that is expected to be read-only in the overlay mount

        payload = 'echo "pwned by overlayfs" > /overlayfs-test/target.txt'
        container.exec_run(payload, privileged=True)

        print("[+] Exploit payload executed: target.txt overwritten")
        return "Executed: overlayfs write attempted"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
