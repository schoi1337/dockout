# attacks/cve_2019_5736.py

def is_vulnerable(env_info):
    """
    Check if the Docker host is likely vulnerable to CVE-2019-5736.
    This CVE affects runC < 1.0.0-rc6.
    """
    runc_version = env_info.get("runc_version", "")
    if not runc_version:
        return False

    # Example logic: consider anything below rc6 vulnerable (simplified)
    if "rc5" in runc_version or "rc4" in runc_version:
        return True
    return False

def run(container):
    print(f"[CVE-2019-5736] Attempting test on container {container.id}...")

    attack_command = "echo 'CVE-2019-5736 test' > /tmp/test.txt"
    result = container.exec_run(attack_command)

    if result.exit_code == 0:
        print("[+] Test successful: /tmp/test.txt created")
        return "Test successful: CVE-2019-5736 test > /tmp/test.txt"
    else:
        print("[-] Test failed")
        return "Test failed"
