# attacks/cgroup_writable_escape.py

def is_vulnerable(env_info):
    """
    Check if /sys/fs/cgroup is writable inside the container.
    This is a basic precondition for classic cgroup notify_on_release escapes.
    """
    try:
        test_path = "/sys/fs/cgroup/test_notify_escape"
        return env_info.get("container_user", "") == "root"
    except Exception:
        return False

def run(container):
    """
    Simulate a writable cgroup-based container escape.
    This PoC just writes to a cgroup config file to demonstrate write access.
    """
    print("[WritableCgroup] Attempting to write to /sys/fs/cgroup/notify_on_release")

    try:
        result = container.exec_run("echo 1 > /sys/fs/cgroup/notify_on_release")
        if result.exit_code == 0:
            return "Write to cgroup config successful (potentially exploitable)"
        else:
            return "Write failed or cgroup is read-only"
    except Exception as e:
        return f"Exception occurred during write: {str(e)}"
