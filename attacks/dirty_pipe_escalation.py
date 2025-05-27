# attacks/dirty_pipe_escalation.py

def is_vulnerable(env_info):
    """
    Dirty Pipe (CVE-2022-0847) affects Linux kernel 5.8 and above.
    We simulate detection by checking kernel version string if available.
    """
    kernel_version = env_info.get("kernel_version", "")
    if not kernel_version:
        return False
    try:
        major, minor = map(int, kernel_version.split('.')[:2])
        return (major == 5 and minor >= 8) or (major > 5)
    except:
        return False

def run(container):
    """
    Simulate Dirty Pipe privilege escalation.
    We do NOT attempt actual kernel exploitation.
    Instead, we simulate file injection to represent overwrite potential.
    """
    print("[DirtyPipe] Simulating privilege escalation attempt...")

    try:
        result = container.exec_run("echo '[SIMULATION] dirty pipe triggered' > /tmp/dirty_pipe_sim.txt")
        if result.exit_code == 0:
            return "Dirty Pipe simulated: wrote /tmp/dirty_pipe_sim.txt"
        else:
            return "Simulation failed: no write access"
    except Exception as e:
        return f"Simulation error: {str(e)}"
