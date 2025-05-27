import docker
import platform

client = docker.from_env()

def get_docker_info():
    try:
        info = client.info()
        version = client.version()
        return {
            "server_version": version.get("Version"),
            "runc_version": version.get("RuncCommit", {}).get("ID", ""),
            "seccomp_enabled": info.get("SecurityOptions", []),
            "rootless": info.get("Rootless"),
            "userns_mode": info.get("SecurityOptions", []),
            "cgroup_driver": info.get("CgroupDriver"),
            "storage_driver": info.get("Driver"),
            "kernel_version": platform.release(),
            "container_user": "root"  # placeholder: actual detection may be improved
        }
    except Exception as e:
        print(f"[!] Failed to get docker environment info: {e}")
        return {}
